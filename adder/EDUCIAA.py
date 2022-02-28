'''

Este archivo, es para agregarlo al repositorio de nmigen_boards/nmigen_boards
Y cuenta con la definicion de los pines de la fpga a usar. En mi caso la EDU-CIAA FPGA
que consta de una fpga Lattice ICE40HX4K TQ44

'''
import subprocess
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from nmigen.build import *
from nmigen.vendor.lattice_ice40 import *
from .resources import *


__all__ = ["EduCiaaPlatform"]


class EduCiaaPlatform(LatticeICE40Platform):
    device      = "iCE40HX4K"
    package     = "TQ144"
    default_clk = "clk100"
    default_rst = "rst"
    resources   = [
        Resource("clk100", 0, Pins("94", dir="i"), Clock(100e6), 
            Attrs( IO_STANDARD="SB_LVCMOS")),
        Resource("rst", 0, Pins("37", dir="io"),
            Attrs(IO_STANDARD="SB_LVCMOS")),

        Resource("r1", 0, Pins("4", dir="o"), Attrs(IO_STANDARD="SB_LVCMOS")),
        Resource("r2", 0, Pins("3", dir="o"), Attrs(IO_STANDARD="SB_LVCMOS")),
        Resource("r3", 0, Pins("2", dir="o"), Attrs(IO_STANDARD="SB_LVCMOS")),
        Resource("r4", 0, Pins("1", dir="o"), Attrs(IO_STANDARD="SB_LVCMOS")),
        Resource("rr", 0, Pins("143", dir="i"), Attrs(IO_STANDARD="SB_LVCMOS")),
        Resource("rv", 0, Pins("144", dir="o"), Attrs(IO_STANDARD="SB_LVCMOS")),

        *ButtonResources(pins="31 32 33 34",       invert=True, attrs=Attrs(IO_STANDARD="SB_LVCMOS")),
        *SwitchResources(pins="99 105 107 95 129 125 122 136", attrs=Attrs(IO_STANDARD="SB_LVCMOS")),

        Resource("a1", 0, Pins("99", dir="i"), Attrs(IO_STANDARD="SB_LVCMOS")),
        Resource("a2", 0, Pins("105", dir="i"), Attrs(IO_STANDARD="SB_LVCMOS")),
        Resource("a3", 0, Pins("107", dir="i"), Attrs(IO_STANDARD="SB_LVCMOS")),
        Resource("ar", 0, Pins("97", dir="o"), Attrs(IO_STANDARD="SB_LVCMOS")),
        Resource("av", 0, Pins("95", dir="i"), Attrs(IO_STANDARD="SB_LVCMOS")),
        
        Resource("b1", 0, Pins("129", dir="i"), Attrs(IO_STANDARD="SB_LVCMOS")),
        Resource("b2", 0, Pins("125", dir="i"), Attrs(IO_STANDARD="SB_LVCMOS")),
        Resource("b3", 0, Pins("122", dir="i"), Attrs(IO_STANDARD="SB_LVCMOS")),
        Resource("br", 0, Pins("134", dir="o"), Attrs(IO_STANDARD="SB_LVCMOS")),
        Resource("bv", 0, Pins("136", dir="i"), Attrs(IO_STANDARD="SB_LVCMOS")),

        UARTResource(0,
            rx="55", tx="56", rts="60", cts="61", dtr="62", dsr="63", dcd="64",
            attrs=Attrs(IO_STANDARD="SB_LVCMOS", PULLUP=1)),

    
    ]
    connectors  = []

    def toolchain_program(self, products, name):
        with products.extract("{}.bin".format(name)) as bitstream_filename:
            subprocess.check_call(["cp", bitstream_filename, "/dev/ttyACM0"])