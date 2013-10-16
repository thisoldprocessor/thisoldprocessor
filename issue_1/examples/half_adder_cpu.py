import unittest

from migen.fhdl.std import Module, Signal
from migen.sim.generic import Simulator, TopLevel


class SumModule(Module):

    def __init__(self):
        self.op_a = Signal()
        self.op_b = Signal()

        self.sum_out = Signal()

        self.comb += self.sum_out.eq(self.op_a ^ self.op_b)


class CarryModule(Module):

    def __init__(self):
        self.op_a = Signal()
        self.op_b = Signal()

        self.carry_out = Signal()

        self.comb += self.carry_out.eq(self.op_a & self.op_b)


class HalfAdderCPU(Module):

    def __init__(self):
        self.op_a = Signal()
        self.op_b = Signal()
        self.sum_out = Signal()
        self.carry_out = Signal()

        self.submodules.sum_module = SumModule()
        self.submodules.carry_module = CarryModule()

        self.comb += [
            self.sum_module.op_a.eq(self.op_a),
            self.sum_module.op_b.eq(self.op_b),
            self.carry_module.op_a.eq(self.op_a),
            self.carry_module.op_b.eq(self.op_b),
            self.sum_out.eq(self.sum_module.sum_out),
            self.carry_out.eq(self.carry_module.carry_out),
        ]


class TestHalfAdderCPU(unittest.TestCase):

    def setUp(self):
        self.cpu = HalfAdderCPU()
        self.sim = Simulator(self.cpu, TopLevel())

    def tearDown(self):
        self.sim.close()

    def testBasic(self):
        self.sim.wr(self.cpu.op_a, 0)
        self.sim.wr(self.cpu.op_b, 0)
        self.sim.run(1)
        self.assertEqual(self.sim.rd(self.cpu.sum_out), 0)
        self.assertEqual(self.sim.rd(self.cpu.carry_out), 0)
        self.sim.wr(self.cpu.op_a, 1)
        self.sim.run(1)
        self.assertEqual(self.sim.rd(self.cpu.sum_out), 1)
        self.assertEqual(self.sim.rd(self.cpu.carry_out), 0)
        self.sim.wr(self.cpu.op_b, 1)
        self.sim.run(1)
        self.assertEqual(self.sim.rd(self.cpu.sum_out), 0)
        self.assertEqual(self.sim.rd(self.cpu.carry_out), 1)


if __name__ == '__main__':
    unittest.main()
