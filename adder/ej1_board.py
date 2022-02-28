from nmigen import *
from nmigen.build import *
from ej1 import *
from nmigen_boards.EDUCIAA import *
       
class SumadorTest(Elaboratable):
    '''Clase para la sintesis en la fpga'''
    
    def elaborate(self, platform):
        a1 = platform.request("a1")
        a2 = platform.request("a2")
        a3 = platform.request("a3")
        av = platform.request("av")
        ar = platform.request("ar")

        r1 = platform.request("r1")
        r2 = platform.request("r2")
        r3 = platform.request("r3")
        r4 = platform.request("r4")
        rv = platform.request("rv")
        rr = platform.request("rr")

        b1 = platform.request("b1")
        b2 = platform.request("b2")
        b3 = platform.request("b3")
        br = platform.request("br")
        bv = platform.request("bv")     

        sum = Sumador(3)

        m = Module()
        m.submodules.sum = sum
        m.d.comb += [
            sum.a.data.eq(Cat([a1, a2, a3])),
            sum.b.data.eq(Cat([b1, b2, b3])),
            Cat([r1, r2, r3, r4]).eq(sum.r.data),
            sum.a.valid.eq(av),
            ar.eq(sum.a.ready),
            sum.b.valid.eq(bv),
            br.eq(sum.b.ready),
            rv.eq(sum.r.valid),
            sum.r.ready.eq(rr)
        ]
        return m

if __name__ == "__main__":
    platform = EduCiaaPlatform()
    platform.build(SumadorTest(), do_program=True)