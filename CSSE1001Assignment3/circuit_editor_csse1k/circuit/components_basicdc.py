"""
Basic DC components. Defined here:
 - IdealCurrentSource
 - IdealResistor
 - IdealVoltageSource
"""

import maths
import math
from base import *

class IdealResistor(Component):
	"""A component subclass representing an ideal passive resistor.
        
        Equation of operation: V = I*R
        """
	def __init__(self, resistance, nickname=None):
		Component.__init__(self, nickname=nickname)
		self.resistance = resistance
		
	def __str__(self):
		return "<ideal resistor: %s>" % self.nickname
		
	def addTo(self, fs):
		"""Applies Ohm's law to this resistor and adds it to the functionset."""
		fs.variables.append(maths.Variable(self, 'I'))
		fs.variables.append(maths.Variable(self, 'V'))
		# this is ohm's law, in =0 form.
		fs.functions.append(lambda v: self.resistance * v[self, 'I'] - v[self, 'V'])
		
class IdealVoltageSource(Component):
	"""A component subclass representing an ideal voltage source.
        
        Equation of operation: V = a"""
	def __init__(self, voltage, nickname=None):
		Component.__init__(self, voltage=voltage, nickname=nickname)
	
	def __str__(self):
		return "<ideal Vsource: %s>" % self.nickname
	
	def addTo(self, fs):
		fs.variables.append(maths.Variable(self, 'I'))
		fs.variables.append(maths.Variable(self, 'V'))
		fs.functions.append(lambda v: v[self, 'V'] - self.voltage)
		
class IdealCurrentSource(Component):
	"""A component subclass representing an ideal voltage source.
        
        Equation of operation: I = a"""
	def __init__(self, current, nickname=None):
		Component.__init__(self, current=current, nickname=nickname)
		
	def __str__(self):
		return "<ideal Isource: %s>" % self.nickname
		
	def addTo(self, fs):
		fs.variables.append(maths.Variable(self, 'I'))
		fs.variables.append(maths.Variable(self, 'V'))
		fs.functions.append(lambda v: v[self, 'I'] - self.current)
		
