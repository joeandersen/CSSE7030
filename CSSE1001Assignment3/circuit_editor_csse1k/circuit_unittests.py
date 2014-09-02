"""Unit tests for the circuit analysis library."""

import unittest
import circuit

class BasicCircuitTest(unittest.TestCase):
	"""A very simple voltage source and resistor circuit. This tests that the solver
	is working at all and that some basic components are available."""
	def setUp(self):
		self.circuit = circuit.Circuit(nickname="c")
		self.vs = circuit.IdealVoltageSource(voltage=5, nickname="vs")
		self.n1 = circuit.Node(nickname="n1")
		self.r1 = circuit.IdealResistor(resistance=10, nickname="r1")
		self.n2 = circuit.Node(nickname="n2")
		
		self.circuit.components = [self.vs, self.r1]
		self.circuit.nodes = [self.n1, self.n2]
		
		self.circuit.connectLoop( [self.vs, self.n1, self.r1, self.n2, self.vs] )
		
	def test_solution(self):
		soln = self.circuit.solve()
		self.assertAlmostEqual(soln[(self.vs, 'V')], 5.00)
		self.assertAlmostEqual(soln[(self.vs, 'I')], -0.5)
		self.assertAlmostEqual(soln[(self.r1, 'V')], 5.00)
		self.assertAlmostEqual(soln[(self.r1, 'I')], 0.5)
		
class VoltageDividerTest(unittest.TestCase):
	def setUp(self):
		self.circuit = circuit.Circuit(nickname="c")
		self.vs = circuit.IdealVoltageSource(voltage=12, nickname="vs")
		self.n1 = circuit.Node(nickname="n1")
		self.r1 = circuit.IdealResistor(resistance=10, nickname="r1")
		self.n2 = circuit.Node(nickname="n2")
		self.r2 = circuit.IdealResistor(resistance=10, nickname="r1")
		self.n3 = circuit.Node(nickname="n3")
		
		self.circuit.components = [self.vs, self.r1, self.r2]
		self.circuit.nodes = [self.n1, self.n2, self.n3]
		
		self.circuit.connectLoop( [self.vs, self.n1, self.r1, self.n2, self.r2, self.n3, self.vs] )
		
	def test_basic_solution(self):
		self.r1.resistance = self.r2.resistance = 10
		soln = self.circuit.solve()
		self.assertAlmostEqual(soln[(self.vs, 'V')], 12.00)
		self.assertAlmostEqual(soln[(self.r1, 'V')], 6.00)
		self.assertAlmostEqual(soln[(self.r2, 'V')], 6.00)
		
	def test_third_solution(self):
		self.r1.resistance = 10
		self.r2.resistance = 20
		soln = self.circuit.solve()
		self.assertAlmostEqual(soln[(self.r1, 'V')], 4.00)
		self.assertAlmostEqual(soln[(self.r2, 'V')], 8.00)
		
class CurrentDividerTest(unittest.TestCase):
	def setUp(self):
		self.circuit = circuit.Circuit(nickname="c")
		self.cs = circuit.IdealCurrentSource(current=1, nickname="cs")
		self.n1 = circuit.Node(nickname="n1")
		self.r1 = circuit.IdealResistor(resistance=1000, nickname="r1")
		self.r2 = circuit.IdealResistor(resistance=1000, nickname="r2")
		self.n2 = circuit.Node(nickname="n2")
		
		self.circuit.components = [self.cs, self.r1, self.r2]
		self.circuit.nodes = [self.n1, self.n2]
		
		self.circuit.connectLoop( [self.cs, self.n1, self.r1, self.n2, self.cs] )
		self.circuit.connectLoop( [self.n1, self.r2, self.n2] )
		
	def test_basic_solution(self):
		self.r1.resistance = self.r2.resistance = 1000
		soln = self.circuit.solve()
		self.assertAlmostEqual(soln[(self.cs, 'I')], 1.0)
		self.assertAlmostEqual(soln[(self.r1, 'I')], -0.5)
		self.assertAlmostEqual(soln[(self.r2, 'I')], -0.5)
		
	def test_tenth_solution(self):
		self.r1.resistance = 900
		self.r2.resistance = 100
		soln = self.circuit.solve()
		self.assertAlmostEqual(soln[(self.r1, 'I')], -0.1)
		self.assertAlmostEqual(soln[(self.r2, 'I')], -0.9)

class Tute3BTest(unittest.TestCase):
	"""A problem taken from ELEC1000 tutorial set 3, University of Queensland.
	This test covers all functionality under List A deliverables."""
	def setUp(self):
		self.circuit = circuit.Circuit(nickname="c")
		
		self.vs = circuit.IdealVoltageSource(voltage=12, nickname="vs")
		self.node_a = circuit.Node(nickname="a")
		self.r1 = circuit.IdealResistor(resistance=10, nickname="r1")
		self.node_b = circuit.Node(nickname="b")
		self.r2 = circuit.IdealResistor(resistance=10, nickname="r2")
		self.r3 = circuit.IdealResistor(resistance=10, nickname="r3")
		self.node_c = circuit.Node(nickname="c")
		self.r4 = circuit.IdealResistor(resistance=10, nickname="r4")
		self.r5 = circuit.IdealResistor(resistance=10, nickname="r5")
		self.node_d = circuit.Node(nickname="d")
		self.cs = circuit.IdealCurrentSource(current=-0.5, nickname="cs")
		self.node_e = circuit.Node(nickname="e", reference=0)
		
		self.circuit.components = [self.vs, self.r1, self.r2, self.r3, self.r4, self.r5, self.cs]
		self.circuit.nodes = [self.node_a, self.node_b, self.node_c, self.node_d, self.node_e]
		
		self.circuit.connectLoop( [self.vs, self.node_a, self.r1, self.node_b, self.r2, self.node_c, 
									self.r3, self.node_d, self.cs, self.node_e, self.vs] )
		self.circuit.connectLoop( [self.node_b, self.r4, self.node_e] )
		self.circuit.connectLoop( [self.node_c, self.r5, self.node_e] )
		
	def test_solution(self):
		soln = self.circuit.solve()
		
		# node voltages
		self.assertAlmostEqual(soln[(self.node_a, 'Vg')], 12)
		self.assertAlmostEqual(soln[(self.node_b, 'Vg')], 5.8)
		self.assertAlmostEqual(soln[(self.node_c, 'Vg')], 5.4)
		self.assertAlmostEqual(soln[(self.node_d, 'Vg')], 10.4)
		
		# component currents
		self.assertAlmostEqual(soln[(self.vs, 'I')], -0.62)
		self.assertAlmostEqual(soln[(self.r1, 'I')], 0.62)
		self.assertAlmostEqual(soln[(self.r4, 'I')], 0.58)
		self.assertAlmostEqual(soln[(self.r2, 'I')], 0.04)
		self.assertAlmostEqual(soln[(self.r5, 'I')], 0.54)
		self.assertAlmostEqual(soln[(self.cs, 'I')], -0.5)
		
	
		
if __name__ == '__main__':
  unittest.main()
		