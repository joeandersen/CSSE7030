"""
Maths utility classes for circuit analysis support.
"""

# It's maths time, children!
# YAY!

import numpy
import scipy.optimize

class Variable:
	"""A variable belonging to a function or variable set.
        
        Constructor: Variable(owner, vartype)
        owner and vartype can be any kind of object, but vartype
        is typically string or integer"""
	def __init__(self, owner, vartype):
		self.owner = owner
		self.vartype = vartype
		
	def __str__(self):
		return repr(self)
				
	def __repr__(self):
		return "<variable %s.%s>" % (repr(self.owner), self.vartype)
		
class VariableNotFoundException(Exception):
        def __init__(self, owner, vartype):
                Exception.__init__(self, "Could not find variable owned by %s having vartype %s." % (owner, vartype))
		
class VariableSet:
	"""A set of variables. This class is the interface seen by functions in
	a FunctionSet for reading parameters, and also is returned
        as the solution to a FunctionSet. Primary access is via subscript operators.
        
        Constructor: VariableSet(list<float>, list<Variable>, list<float>)"""
	def __init__(self, array, varlist, error=None):
		self.array = array
		self.varlist = varlist
		self.error = error
		
	def __getitem__(self, tup):
		"""
		Syntax: vset[owner, vartype]
		or vset[variable]
		
		Retrieve the variable value from this set owned by owner and having type vartype.
		"""
		# if we're sent a variable directly, just go grab it
		if tup in self.varlist:
			return self.array[self.varlist.index(tup)]
		else:
			# othewise, run a search
			owner, vartype = tup
			for v in self.varlist:
				if v.owner == owner and v.vartype == vartype:
					return self.array[self.varlist.index(v)]
                        # can't find it? raise an exception
                        raise VariableNotFoundException(owner, vartype)
                        
        def __repr__(self):
                return str(self)
                
        def __str__(self):
                return "<VariableSet: ["+", ".join(["%s = %s" % (v, self[v]) for v in self.varlist])+"]>"
				
	def keys(self):
                """Returns the list of variables in the set."""
		return self.varlist
		
	def errorOn(self, var):
                """Returns the error figure recorded for a given variable."""
		return self.error[self.varlist.index(var)]
		
	def values(self):
                """Returns the array of values of all variables in the set."""
		return self.array

class FunctionSet:
	"""The workhorse class of the maths module. This class represents a series of functions
	that must be optimized according to their variables. It uses least-squares fitting from
	SciPy to achieve this.
	
	Typically, this is used for solving non-linear simultaneous equations, of the form:
		f(x,y)=0
		g(x,y)=0
	where f and g are some non-linear function of the two variables x and y.
	
	An example:
	We will solve the system above where f(x,y)=x^2-y^3 and g(x,y)=2*x+y-18. We create the variables
	as follows:
		fs = FunctionSet()
		
		x = Variable(fs, 'x')
		y = Variable(fs, 'y')
		fs.variables = [x,y]
		
	Then the functions:
		f = lambda vset: vset[fs,'x']*2 - vset[fs,'y']*3
		g = lambda vset: vset[fs,'x'] - vset[fs,'y'] - 1
		fs.functions = [f,g]
		
		soln = fs.optimize()
		==> <VariableSet: [<variable <functionset>.x> = 3.0, <variable <functionset>.y> = 2.0]>
	"""
	def __init__(self):
		self.functions = []
		self.variables = []
		
	def __repr__(self):
		return "<functionset>"
		
	def _optimizerFunc(self, args):
                """Internal function used by the optimizer. Returns the error array associated with a 
                given set of variable values."""
		varset = VariableSet(args, self.variables)
		return [f(varset) for f in self.functions]
		
	def optimize(self):
		"""Attempts to solve the system using the Levenberg-Marquadt algorithm.
                
                FunctionSet#optimize() -> VariableSet"""
		start_vector = [1.]*len(self.variables)
		result = scipy.optimize.leastsq(self._optimizerFunc, start_vector, full_output=1)
		return VariableSet(result[0],self.variables,self._optimizerFunc(result[0]))
		