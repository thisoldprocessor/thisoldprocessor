import unittest

from migen.fhdl.std import Module, Signal
from migen.sim.generic import Simulator, TopLevel


class OrCPU(Module):

    def __init__(self):
        self.a = Signal()
        self.b = Signal()
        self.x = Signal()

        self.comb += self.x.eq(self.a | self.b)


class TestOrCPU(unittest.TestCase):

    def setUp(self):
        self.cpu = OrCPU()
        self.sim = Simulator(self.cpu, TopLevel())

    def tearDown(self):
        self.sim.close()

    def testBasic(self):
        self.sim.wr(self.cpu.a, 0)
        self.sim.wr(self.cpu.b, 0)
        self.sim.run(1)
        self.assertEqual(self.sim.rd(self.cpu.x), 0)
        self.sim.wr(self.cpu.a, 1)
        self.sim.run(1)
        self.assertEqual(self.sim.rd(self.cpu.x), 1)
        self.sim.wr(self.cpu.b, 1)
        self.sim.run(1)
        self.assertEqual(self.sim.rd(self.cpu.x), 1)


if __name__ == '__main__':
    unittest.main()
