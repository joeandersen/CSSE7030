"""
Diode components, shockley ideal and red and yellow lab LEDs.
"""

import maths
import math
from base import *

class ShockleyDiode(Component):
	"""A component subclass representing a diode obeying the Shockley equation.
	
	Parameters:
		saturation_current (default = 1e-12)
		thermal_voltage (default = 25.85e-03, value at 300K)
		e_coeff = ideality coefficient (usually 1-2 in silicon diodes) (default = 1)
                
        Equation of operation:
                I = Is*(exp(V/(e_coeff*thermal_v))-1)
	"""
	def __init__(self, saturation_current=1e-12, thermal_voltage=25.85e-03, e_coeff=1.00, nickname=None):
		Component.__init__(self, nickname=nickname)
		self.saturation_current = saturation_current
		self.thermal_voltage = thermal_voltage
		self.e_coeff = e_coeff
		
	def __str__(self):
		return "<shockley diode: %s>" % self.nickname
		
	def addTo(self, fs):
		fs.variables.append(maths.Variable(self, 'I'))
		fs.variables.append(maths.Variable(self, 'V'))
		fs.functions.append(lambda v: self.saturation_current * (math.exp(v[self,'V']/(self.e_coeff*self.thermal_voltage))-1) - v[self,'I'])
		
class RedLED(ExpFitComponent):
	"""A 3mm red lab LED modelled on data collected between 1 and 25 mA. 
	This is a strictly empirical model, taking no parameters.
        
        Model values:
                a = 1.7437436e-04 
                b = 2.3425274e+00
                c = 3.4204351e-01
                d = -1.190421e-02
        """
	
	def __init__(self, nickname=None, flip=False):
		ExpFitComponent.__init__(self, 
			a = 1.7437436e-04, 
			b = 2.3425274e+00,
			c = 3.4204351e-01,
			d = -1.190421e-02, nickname=nickname)
		if flip:
			self.ends.reverse()

	def __str__(self):
		return "<red led: %s>" % self.nickname
		
class YellowLED(ExpFitComponent):
	"""A 3mm yellow/green lab LED modelled on data collected between 1 and 25 mA.
	This is a strictly empirical model, taking no parameters.
        
        Model values:
                a = 1.579071883013601e-04
                b = 2.387399288036779e+00
                c = 3.602120875180140e-01
                d = -1.798387060828336e-02
        """
	
	def __init__(self, nickname=None):
		ExpFitComponent.__init__(self, 
			a = 1.579071883013601e-04,
			b = 2.387399288036779e+00,
			c = 3.602120875180140e-01,
			d = -1.798387060828336e-02, nickname=nickname)
		
	def __str__(self):
		return "<yellow led: %s>" % self.nickname