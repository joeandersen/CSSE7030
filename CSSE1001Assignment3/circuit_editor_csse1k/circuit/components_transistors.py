"""
Transistor components.
"""

# note that this never really got anywhere.
# it's kinda just cruft sitting on the end of the library.
# eat it if you like. it may or may not be tasty.

import maths
import math
from base import *

class EbersMollTransistor(Component):
	"""A base-junction transistor component using the Ebers-Moll BJT model.
	
	Assumption: first connection is collector, second emitter, third base.
	
	Parameters:
		bf = forward common emitter current gain (20-500)
		br = reverse common emitter current gain (0-20)
		i_s = reverse saturation current (e-15 to e-12)
		vt = thermal voltage (25.85mV at 300K)
	"""
	def __init__(self, bf=50, br=10, i_s=1e-12, vt=25.85e-03):
		Component.__init__(self, maxEnds=3)
		self.bf = bf
		self.br = br
		self.i_s = i_s
		self.vt = vt
		
	def __str__(self):
		return "<ebers-moll transistor: %s>" % self.nickname
		
	def nodeCurrentCoefficient(self, node):
		"""The coefficient of current through this component from the perspective of a given node."""
		return {0: 1, 1: -1, 2: 1}[self.ends.index(node)]
		
	def nodeVoltageCoefficient(self, node):
		"""The coefficient of voltage across this component from the perspective of a given node."""
		return {0: 1, 1: -1, 2: 1}[self.ends.index(node)]
		
	def addTo(self, fs):
		fs.variables.append(maths.Variable(self, "Ic"))
		fs.variables.append(maths.Variable(self, "Ib"))
		fs.variables.append(maths.Variable(self, "Ie"))
		fs.variables.append(maths.Variable(self, "Vbe"))
		fs.variables.append(maths.Variable(self, "Vbc"))
		
	