from nmigen import *
from nmigen_cocotb import run
import cocotb
from cocotb.triggers import RisingEdge, Timer
from cocotb.clock import Clock
from random import randint


class Stream(Record):
    def __init__(self, width, **kwargs):
        Record.__init__(self, [('data', signed(width)), ('valid', 1), ('ready', 1)], **kwargs)

    def accepted(self):
        return self.valid & self.ready

    class Driver:
        def __init__(self, clk, dut, prefix):
            self.clk = clk
            self.data = getattr(dut, prefix + 'data')
            self.valid = getattr(dut, prefix + 'valid')
            self.ready = getattr(dut, prefix + 'ready')

        async def send(self, data):
            self.valid <= 1
            for d in data:
                self.data <= d
                await RisingEdge(self.clk)
                while self.ready.value == 0:
                    await RisingEdge(self.clk)
            self.valid <= 0

        async def recv(self, count):
            self.ready <= 1
            data = []
            for _ in range(count):
                await RisingEdge(self.clk)
                while self.valid.value == 0:
                    await RisingEdge(self.clk)
                data.append(self.data.value.integer)
            self.ready <= 0
            return data
            print (data)


class Sumador(Elaboratable):
    '''Sumador de n bits a definir durante la instanciacion con el resultado en n+1 bits

    Parameters
    ----------
    width: int
        Cantidad de bits de los numeros a sumar
    '''
    def __init__(self, width):
        self.a = Stream(width, name='a')
        self.b = Stream(width, name='b')
        self.r = Stream((width + 1), name='r')

    def elaborate(self, platform):
        m = Module()
        sync = m.d.sync
        comb = m.d.comb

        with m.If(self.a.accepted() & self.b.accepted() & self.r.ready):
            sync += self.r.data.eq(self.a.data + self.b.data)

        with m.If(self.a.accepted() & self.b.accepted()):
            sync += self.r.valid.eq(1)
        comb += [    
            self.a.ready.eq(self.a.valid & self.b.valid),
            self.b.ready.eq(self.a.valid & self.b.valid)
        ]
        return m


async def init_test(dut):
    cocotb.fork(Clock(dut.clk, 10, 'ns').start())
    dut.rst <= 1
    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)
    dut.rst <= 0


@cocotb.test()
async def burst(dut):
    await init_test(dut)

    stream_input_a = Stream.Driver(dut.clk, dut, 'a__')
    stream_input_b = Stream.Driver(dut.clk, dut, 'b__')
    stream_output = Stream.Driver(dut.clk, dut, 'r__')

    expected = []
    N = 10
    width_a = len(dut.a__data)
    width_b = len(dut.b__data)
    mask_a = int('1' * (width_a), 2)
    mask_b = int('1' * (width_b), 2)

    if width_a > width_b:
        mask = mask_a
    else:
        mask = mask_b

    range_a = int(((2 ** width_a) - 1) / 2)
    range_b = int(((2 ** width_b) - 1) / 2)
    data_a = [randint(-range_a,range_a) for _ in range(N)]
    data_b = [randint(-range_b,range_b) for _ in range(N)]
    
    for i in range(len(data_a)):
        expected.append((data_a[i] + data_b[i]) & mask)
    
    cocotb.fork(stream_input_a.send(data_a))
    await Timer(5, units="ns")
    cocotb.fork(stream_input_b.send(data_b))
    recved = await stream_output.recv(N) 
    for i in range(len(recved)):
        aux = recved[i] & mask
        recved[i] = aux

    assert recved == expected
    
    

if __name__ == '__main__':
    core = Sumador(3)
    run(
        core, 'ej1',
        ports=
        [
            *list(core.a.fields.values()),
            *list(core.b.fields.values()),
            *list(core.r.fields.values())
        ],
        vcd_file='ej1.vcd'
    )