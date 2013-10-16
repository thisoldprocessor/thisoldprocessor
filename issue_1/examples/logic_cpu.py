import unittest

from migen.fhdl.std import Module, Signal, Cat
from migen.sim.generic import Simulator, TopLevel


class LogicCPU(Module):

    def __init__(self):
        self.a = Signal(8)
        self.b = Signal(8)
        self.x = Signal(8)

        a_and_b = Signal()
        a_or_b = Signal()
        a_xor_b = Signal()
        a_nand_b = Signal()
        a_nor_b = Signal()
        a_xnor_b = Signal()
        not_a = Signal()

        self.comb += [
            a_and_b.eq(self.a[0] & self.b[0]),
            a_or_b.eq(self.a[1] | self.b[1]),
            a_xor_b.eq(self.a[2] ^ self.b[2]),
            a_nand_b.eq(~(self.a[3] & self.b[3])),
            a_nor_b.eq(~(self.a[4] | self.b[4])),
            a_xnor_b.eq(~(self.a[5] ^ self.b[5])),
            not_a.eq(~self.a[6]),
            self.x.eq(Cat(a_and_b, a_or_b, a_xor_b, a_nand_b, a_nor_b, a_xnor_b, not_a, self.b[7])),
        ]


class TestLogicCPU(unittest.TestCase):

    def setUp(self):
        self.cpu = LogicCPU()
        self.sim = Simulator(self.cpu, TopLevel())

    def tearDown(self):
        self.sim.close()

    def testBasic(self):
        self.sim.wr(self.cpu.a, 0)
        self.sim.wr(self.cpu.b, 0)
        self.sim.run(1)
        self.assertEqual(self.sim.rd(self.cpu.x), 0b01111000)
        self.sim.wr(self.cpu.a, 0xff)
        self.sim.run(1)
        self.assertEqual(self.sim.rd(self.cpu.x), 0b00001110)
        self.sim.wr(self.cpu.a, 0)
        self.sim.wr(self.cpu.b, 0x0f)
        self.sim.run(1)
        self.assertEqual(self.sim.rd(self.cpu.x), 0b01111110)
        self.sim.wr(self.cpu.a, 0xf0)
        self.sim.run(1)
        self.assertEqual(self.sim.rd(self.cpu.x), 0b00001110)


if __name__ == '__main__':
    unittest.main()
