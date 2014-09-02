"""
Base classes for circuit analysis (other than maths ones)
Defined here: exceptions for the analysis, base classes
              for circuit components, connections between,
              as well as ideal ammeters and voltmeters.
"""

# yes, importing maths then math is confusing. my bad.
import maths
import math

class EndCountException(Exception):
	"""An exception raised when a new connection is made, indicating that a circuit element 
	already has all of its ends connected."""
	def __init__(self):
		Exception.__init__(self, "Too many ends have been added to this component.")
		
class SolverException(Exception):
        """An exception raised when a system of equations has no feasible solution."""
	def __init__(self, error, epsilon):
		Exception.__init__(self, "The circuit could not be solved. Error was %.12f, which is above the given epsilon value of %.12f."%(error,epsilon))

class Connection:
	"""Represents a connection between a component and a node.
        
        Parameters to constructor:
                coeff: the loop coefficient of this connection. an integer that is either
                       -1 or +1 depending on whether the represented pin is considered to be entering 
                       or leaving the component.
                voltage: the vartype of voltage across the component from the perspective of
                         this connection
                current: the vartype of current through the component
                """
	def __init__(self, component, coeff=1, nickname=None, voltage=None, current=None):
		self.coeff = coeff
		self.voltage = voltage
		self.current = current
		self.nickname = nickname
		self.component = component
		self.node = None
		
	def __repr__(self):
		return self.__str__()
	
	def __str__(self):
		return "<connection>"
		
	def connect(self, node):
                """Connect to a node."""
		self.node = node
		
	def disconnect(self):
		self.node.ends.remove(self)
		self.node = None
		
	def next(self, fromitem):
                """Returns the next component or node in the loop starting from the given item."""
		return [x for x in [self.component, self.node] if x != fromitem]
		
	def getV(self, varset):
                """Gets the loop voltage drop of this connection."""
		return self.coeff * varset[self.component, self.voltage]
	
	def getI(self, varset):
                """Gets the current into the node this connection connects to."""
		return -1 * self.coeff * varset[self.component, self.current]
		

class Component:
	"""Superclass for circuit components. You should always instantiate an individual
	component rather than this superclass."""
	def __init__(self, current=0, voltage=0, maxEnds=2, nickname=None):
		"""Basic template functions represent an element that controls both the current and voltage
		across it."""
		# create ends for the component
		# note that coeff represents the coefficient of voltage looking from
		# the node towards the component, so on the positive end of the component,
		# the end coefficient is negative
		self.ends = [Connection(self, coeff=-1, voltage='V', current='I', nickname="+"), 
					Connection(self, voltage='V', current='I', nickname="-")]
		
		self.current = current
		self.voltage = voltage
		
		self.nickname = nickname
		
	def __repr__(self):
		return self.__str__()
		
	def __str__(self):
		return "<component: %s>" % self.nickname
		
	def orientation(self):
		return "%s -> %s" % (self.ends[0].node.nickname, self.ends[1].node.nickname)
		
	def connect(self, node):
		"""Connects this component to a node. Note this is a one-way connection."""
		for e in self.ends:
			if e.node == None:
				e.connect(node)
				return e
		raise EndCountException()
		
	def connectWith(self, node):
                """Asks the given node to connect with this component."""
		node.connectWith(self)
		
	def disconnect(self):
		for e in self.ends:
			e.disconnect()
		
	def next(self, fromnode):
		"""A list of potential next nodes in a loop spanning fromnode and this component."""
		return [e for e in self.ends if e != fromnode]

	def addTo(self, fs):
		"""Adds the equations involving this component to the functionset."""
		print "WARNING: the addTo function has not been overloaded in %s" % self
		fs.variables.append(maths.Variable(self, 'V'))
		fs.variables.append(maths.Variable(self, 'I'))
		# dummy functions, constrain our voltage and current to zero
		# this way, any component forgetting to override this method
		# will most likely result in an impossible circuit
		fs.functions.append(lambda vset: vset[self, 'V']-self.voltage)
		fs.functions.append(lambda vset: vset[self, 'I']-self.current)
		
class IdealAmmeter(Component):
	"""A component used as an ideal ammeter -- dissipates no voltage, and allows 
        arbitrary current.
        
        Equation of operation: V = 0
        """
	def __init__(self, nickname=None):
		Component.__init__(self, nickname=nickname)
		
	def __str__(self):
		return "<ammeter: %s>" % self.nickname
		
	def addTo(self, fs):
		fs.variables.append(maths.Variable(self, 'V'))
		fs.variables.append(maths.Variable(self, 'I'))
		# constrain our voltage to zero (ideal ammeter dissipates no voltage)
		fs.functions.append(lambda vset: vset[self, 'V'])
		
class IdealVoltmeter(Component):
	"""A component used as an ideal voltmeter -- allows no current, and dissipates
        an arbitrary voltage.
        
        Equation of operation: I = 0
        """
	def __init__(self, nickname=None):
		Component.__init__(self, nickname=nickname)
		
	def __str__(self):
		return "<voltmeter: %s>" % self.nickname
		
	def addTo(self, fs):
		fs.variables.append(maths.Variable(self, 'V'))
		fs.variables.append(maths.Variable(self, 'I'))
		# constrain our current to zero (ideal voltmeter uses no current)
		fs.functions.append(lambda vset: vset[self, 'I'])
		
class ExpFitComponent(Component):
	"""A component based on an empirical exponential fit model. This is good for use with diodes.
	The equation used is:
		I = a*exp(b*V_component + c)+d
	"""
	
	def __init__(self, a, b, c, d, nickname=None):
		Component.__init__(self, nickname=nickname)
		# define the parameters to the exp function
		self.a = a
		self.b = b
		self.c = c
		self.d = d
	
	def __str__(self):
		return "<fit component: %s>" % self.nickname
		
	def addTo(self, fs):
		fs.variables.append(maths.Variable(self, 'I'))
		fs.variables.append(maths.Variable(self, 'V'))
		fs.functions.append(lambda v: (self.a*math.exp(self.b*v[self,'V']+self.c)+self.d)-v[self,'I'])
		
class Node:
	"""A node in the circuit."""
	def __init__(self, nickname=None, reference=None):
		self.ends = []
		self.reference = reference
		self.nickname = nickname
		
	def __repr__(self):
		return self.__str__()
		
	def __str__(self):
		return "<node: %s>" % self.nickname
		
	def orientation(self):
		return "undefined"
		
	def disconnectAll(self):
		for e in self.ends:
			e.disconnect()
		
	def connect(self, connection):
		"""Connects this node to a component. Note this is a one-way connection.
		For two-way connections, use connectWith, or Circuit.connectLoop."""
		self.ends.append(connection)
	
	def connectWith(self, component):
		"""Constructs a 2-way connection between this node and the given component."""
		self.connect(component.connect(self))
		
	def next(self, fromcomponent):
		"""Returns possible next components in a loop containing fromcomponent and this node."""
		return [c for c in self.ends if c != fromcomponent]
		
	def addTo(self, fs):
		"""Apply KCL to this node, and add the resulting equation to the functionset."""
		# sum of currents into node = 0
		fs.variables.append(maths.Variable(self, 'Vg'))
		if self.reference != None:
			fs.functions.append(lambda v: v[self, 'Vg'] - self.reference)
		fs.functions.append(lambda v: sum([e.getI(v) for e in self.ends]))
		
class Circuit:
	"""Represents a basic DC circuit."""
	def __init__(self,nickname = None):
		self.nodes = []
		self.components = []
		self.nickname = nickname
		
	def __str__(self):
		return "<circuit: %s>" % self.nickname
		
	def addNode(self, node):
		"""Adds a node to the circuit. Does not connect it."""
		self.nodes.append(node)
		
	def addComponent(self, component):
		self.components.append(component)
		
	def walk(self, loop, point):
		"""A recursive walking function, used for constructing KVL loops."""
		if point in loop:
			if point == loop[0]:
				if not loop in self.loops:
					self.loops.append(loop)
			return 
		ps = point.next(loop[-1])
		for p in ps:
			self.walk( loop+[point], p )
		
	def addLoopsTo(self, fs):
		"""Apply KVL in all available loops of this circuit, and place the resulting functions into the 
		functionset."""
		
		# this is probably one of the most complex methods in the library
		# first, create two anonymous classes to execute the constraints
		# based on loops and branches
		
		class AnonymousLoopRunner:
			def __init__(self, loop):
				self.loop = loop
			def kvlComponents(self, v):
				sum = 0
				done = []
                                # go around the loop summing voltages
				for i in self.loop:
					if i.__class__ == Connection:
						if i.component not in done:
							sum += i.getV(v)
						done.append(i.component)
				return sum			
						
		class AnonymousBranchRunner:
			def __init__(self, branch):
				self.branch = branch[1:-1]
				self.start = branch[0]
				self.end =  branch[-1]
				
			def kvlNodes(self, v):
				voltage = v[self.start, 'Vg']
				done = []
                                # sum voltage drops down the branch to establish
                                # relationships between nodes relative to ground
				for i in self.branch:
					if i.__class__ == Connection and i.component not in done:
						voltage += i.getV(v)
						done.append(i.component)
				voltage -= v[self.end, 'Vg']
				return voltage
				
		# now begin gathering loops
		self.loops = []
		self.walk([self.components[0].ends[0]], self.components[0])
		
		# now, take the loops and create looprunners
		for loop in self.loops:
			fs.functions.append(AnonymousLoopRunner(loop).kvlComponents)
			
			# take apart each branch of the loop and create a branchrunner for it
			lastNode = None
			for n in range(0,len(loop)):
				i = loop[n]
				if i in self.nodes:
					if lastNode == None:
						lastNode = n
					else:
						il = loop[lastNode]		
						fs.functions.append(AnonymousBranchRunner(loop[lastNode:n+1]).kvlNodes)
						lastNode = n
					

	def getFunctionSet(self):
		"""Returns the functionset representing all the restraints on this circuit."""
		fs = maths.FunctionSet()
		for c in self.components:
			c.addTo(fs)
		for n in self.nodes:
			n.addTo(fs)
		self.addLoopsTo(fs)
		return fs
		
	def equivProbe(self, points):
		"""Perform an equivalence probe on the specified nodes (used by Thevenin/Norton
		solvers. Returns (V_oc, I_sc)."""
		# probe me! probe me please!
		
		# get open circuit voltage
		vm = IdealVoltmeter()
		self.components.append(vm)
		self.connectLoop([points[0], vm, points[1]])
		# solve for the voltage on the meter
		voc = self.solve()[vm, 'V']
		# disconnect the voltmeter
		vm.disconnect()
		self.components.remove(vm)
		
		# now get short-circuit current
		amm = IdealAmmeter()
		self.components.append(amm)
		self.connectLoop([points[1], amm, points[0]])
		# solve, and get the current on the meter
		isc = self.solve()[amm, 'I']
		# disconnect the meter
		amm.disconnect()
		self.components.remove(amm)
		
		# return the values
		return (voc, isc)
		
	def solveThevenin(self, points):
		"""Uses the two open-circuit nodes given to solve for a Thevenin equivalent
		voltage and resistance to this circuit."""
		voc,isc = self.equivProbe(points)
		
		# return a tuple of voltage and resistance
		return (voc, -voc/isc)
	
	def solveNorton(self, points):
		"""Uses two open-circuit nodes given to solve for a Norton equivalent
		current and resistance to this circuit."""
		# use the probe function
		voc,isc = self.equivProbe(points)
		# return current and resistance
		return (-isc, -voc/isc)
		
	def solve(self, epsilon=1e-10):
		"""Solves the given circuit to return a solution list."""
		fs = self.getFunctionSet()
		v = fs.optimize()
		error = sum([abs(v.errorOn(x)) for x in v.keys()])
		if error > epsilon:
			raise SolverException(error, epsilon)
		return v
		
        def printableSolution(self):
                """Gives the solution in a human-readable pretty-print format suitable
                for printing."""
                try:
			soln = self.solve()
		except SolverException, e:
			return str(e)

                ostr = ""
		ostr += "SOLUTION:\n" + "-"*30 +"\n"
		for x in soln.keys():
			ostr += "%25s%3s = %.4f\t{%s}\n" % (x.owner, x.vartype, soln[x], x.owner.orientation())
                        
                return ostr
		
	def printSolution(self):
		"""Prints the solution to the circuit in a nice, human-readable format."""
		print self.printableSolution()
				
	def connectLoop(self, loop):
		"""Connects, in order, all elements of loop."""
		for i in range(0,len(loop)-1):
			if not loop[i+1] in [x.next(loop[i]) for x in loop[i].ends]:
				loop[i].connectWith(loop[i+1])
