import magma as m


def test_sum_basic():
    class T(m.Sum):
        x = m.Bit
        y = m.Bits[2]

    class Foo(m.Circuit):
        io = m.IO(I=m.In(T), O=m.Out(T))
        with m.match(io.I, T.x):
            io.O.x @= ~io.I.x
        with m.match(io.I, T.y):
            io.O.y @= io.I.y ^ 0b11
