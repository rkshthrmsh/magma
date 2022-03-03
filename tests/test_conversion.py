import pytest
import magma as m
import hwtypes as ht


def _assert_identical(x, y):
    assert all(xi is yi for xi, yi in zip(x, y))


def test_concat_basic():
    x = m.Bit(1)
    y = m.Bits[1](1)
    o0 = m.concat(x, y)
    o1 = m.concat(m.bits(x), y)
    _assert_identical(o0, o1)
    _assert_identical(o0, [x, y[0]])


def test_concat_bit():
    x = ht.Bit(True)
    y = True
    z = m.Bits[1](1)
    o = m.concat(x, y, z)
    assert o.const()
    _assert_identical(o, [m.Bit.VCC] * 3)


def test_ext():
    x0 = m.SInt[1](1)

    x1 = m.zext_by(x0, 2)
    x2 = m.zext_to(x0, 3)
    assert isinstance(x1, m.SInt)
    assert isinstance(x2, m.SInt)
    assert x1.const()
    _assert_identical(x1, x2)
    _assert_identical(x1, [m.Bit.VCC, m.Bit.GND, m.Bit.GND])

    x3 = m.sext_by(x0, 2)
    x4 = m.sext_to(x0, 3)
    assert isinstance(x3, m.SInt)
    assert isinstance(x4, m.SInt)
    assert x3.const()
    _assert_identical(x3, x4)
    _assert_identical(x3, [m.Bit.VCC] * 3)


def test_concat_type_error():
    with pytest.raises(TypeError):
        m.concat(object(), object())


@pytest.mark.parametrize('op', [m.uint, m.sint])
def test_convert_extend(op):
    x = m.Bits[5]()
    o = op(x, 32)
    assert len(o) == 32
    if op is m.sint:  # check sext logic
        hi = o[5:]
        _assert_identical(hi, [x[4]] * len(hi))
