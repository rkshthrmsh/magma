import pytest

import magma as m


class _MixedTuple(m.Product):
    x = m.In(m.Bit)
    y = m.Out(m.Bit)


def _make_io():
    return m.IO(
        I=m.In(m.Bit),
        I0=m.In(m.Array[8, m.Bits[10]]),
        mixed=_MixedTuple,
        O=m.Out(m.Bit),
        O3=m.Out(m.Array[4, m.Bits[6]]),
    )


def _get_inputs(obj):
    yield obj.O
    yield obj.mixed.y
    yield from obj.O3


def _get_outputs(obj):
    yield obj.I
    yield from obj.I0
    yield obj.mixed.x


def _check_open_not_implemented(cls):
    with pytest.raises(NotImplementedError):
        cls.open()


def test_stubify_ckt():

    class _Foo(m.Circuit):
        io = _make_io()

    m.stubify(_Foo)

    assert m.isdefinition(_Foo)
    _check_open_not_implemented(_Foo)
    drivers = (port.trace() for port in _get_inputs(_Foo))
    assert all(driver.const() and int(driver) == 0 for driver in drivers)


def test_decorator():

    @m.circuit_stub
    class _Foo(m.Circuit):
        io = _make_io()

    assert m.isdefinition(_Foo)
    _check_open_not_implemented(_Foo)
    drivers = (port.trace() for port in _get_inputs(_Foo))
    assert all(driver.const() and int(driver) == 0 for driver in drivers)


def test_subclass():

    class _Foo(m.CircuitStub):
        io = _make_io()

    assert m.isdefinition(_Foo)
    _check_open_not_implemented(_Foo)
    drivers = (port.trace() for port in _get_inputs(_Foo))
    assert all(driver.const() and int(driver) == 0 for driver in drivers)


def test_io():

    class _Foo(m.Circuit):
        io = _make_io()
        m.stubify(io)

    assert m.isdefinition(_Foo)
    drivers = (port.trace() for port in _get_inputs(_Foo))
    assert all(driver.const() and int(driver) == 0 for driver in drivers)
