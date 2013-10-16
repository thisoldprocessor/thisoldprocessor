import unittest

from migen.fhdl.std import Module, Signal
from migen.sim.generic import Simulator, TopLevel

from .full_adder_cpu import FullAdderCPU


class FourBitAdderCPU(Module):

    def __init__(self):
        self.op_a = Signal(4)
        self.op_b = Signal(4)
        self.sum_out = Signal(4)


class TestFourBitAdderCPU(unittest.TestCase):

    def setUp(self):
        self.cpu = FourBitAdderCPU()
        self.sim = Simulator(self.cpu, TopLevel())

    def tearDown(self):
        self.sim.close()

    def testBasic(self):
        self.sim.wr(self.cpu.op_a, 0)
        self.sim.wr(self.cpu.op_b, 0)
        self.sim.run(1)
        self.assertEqual(self.sim.rd(self.cpu.sum_out), 0)
        self.sim.wr(self.cpu.op_a, 1)
        self.sim.run(1)
        self.assertEqual(self.sim.rd(self.cpu.sum_out), 1)
        self.sim.wr(self.cpu.op_b, 1)
        self.sim.run(1)
        self.assertEqual(self.sim.rd(self.cpu.sum_out), 2)
        self.sim.wr(self.cpu.op_b, 2)
        self.sim.run(1)
        self.assertEqual(self.sim.rd(self.cpu.sum_out), 3)
        self.sim.wr(self.cpu.op_a, 12)
        self.sim.run(1)
        self.assertEqual(self.sim.rd(self.cpu.sum_out), 14)
        self.sim.wr(self.cpu.op_b, 5)
        self.sim.run(1)
        self.assertEqual(self.sim.rd(self.cpu.sum_out), 1)


if __name__ == '__main__':
    unittest.main()
