import unittest

from migen.fhdl.std import Module, Signal
from migen.sim.generic import Simulator, TopLevel


class FullAdderCPU(Module):

    def __init__(self):
        self.op_a = Signal()
        self.op_b = Signal()
        self.carry_in = Signal()
        self.sum_out = Signal()
        self.carry_out = Signal()


class TestFullAdderCPU(unittest.TestCase):

    def setUp(self):
        self.cpu = FullAdderCPU()
        self.sim = Simulator(self.cpu, TopLevel())

    def tearDown(self):
        self.sim.close()

    def testBasic(self):
        self.sim.wr(self.cpu.op_a, 0)
        self.sim.wr(self.cpu.op_b, 0)
        self.sim.wr(self.cpu.carry_in, 0)
        self.sim.run(1)
        self.assertEqual(self.sim.rd(self.cpu.sum_out), 0)
        self.assertEqual(self.sim.rd(self.cpu.carry_out), 0)
        self.sim.wr(self.cpu.op_a, 1)
        self.sim.run(1)
        self.assertEqual(self.sim.rd(self.cpu.sum_out), 1)
        self.assertEqual(self.sim.rd(self.cpu.carry_out), 0)
        self.sim.wr(self.cpu.op_a, 0)
        self.sim.wr(self.cpu.carry_in, 1)
        self.sim.run(1)
        self.assertEqual(self.sim.rd(self.cpu.sum_out), 1)
        self.assertEqual(self.sim.rd(self.cpu.carry_out), 0)
        self.sim.wr(self.cpu.op_b, 1)
        self.sim.run(1)
        self.assertEqual(self.sim.rd(self.cpu.sum_out), 0)
        self.assertEqual(self.sim.rd(self.cpu.carry_out), 1)
        self.sim.wr(self.cpu.op_a, 1)
        self.sim.run(1)
        self.assertEqual(self.sim.rd(self.cpu.sum_out), 1)
        self.assertEqual(self.sim.rd(self.cpu.carry_out), 1)


if __name__ == '__main__':
    unittest.main()
