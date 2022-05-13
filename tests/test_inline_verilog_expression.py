import pytest

import magma as m
import magma.testing


class _RegWrapper(m.Circuit):
    name = "RegWrapper"
    io = m.IO(
        I=m.In(m.Bit),
        O=m.Out(m.Bit),
    ) + m.ClockIO()
    m.inline_verilog(
        "reg [0:0] R;\nasssign R <= {I};\n",
        I=io.I
    )
    io.O @= m.InlineVerilogExpression("R | I", m.Bit)()


def test_basic():
    expected = \
"""RegWrapper = DefineCircuit("RegWrapper", "I", In(Bit), "O", Out(Bit), "CLK", In(Clock))
InlineVerilogExpression_a489b4461c0192fc_inst0 = InlineVerilogExpression_a489b4461c0192fc()
_RegWrapper_inline_verilog_inst_0 = _RegWrapper_inline_verilog_0(name="_RegWrapper_inline_verilog_inst_0")
_magma_inline_wire0 = Wire(name="_magma_inline_wire0")
wire(_magma_inline_wire0.out, _RegWrapper_inline_verilog_inst_0.__magma_inline_value_0)
wire(RegWrapper.I, _magma_inline_wire0.in)
wire(InlineVerilogExpression_a489b4461c0192fc_inst0.O, RegWrapper.O)
EndCircuit()"""
    assert repr(_RegWrapper) == expected


@pytest.mark.parametrize("output", ("coreir-verilog", "mlir",))
def test_compilation(output):
    basename = f"{_RegWrapper.name}_{output}"
    m.compile(f"build/{basename}", _RegWrapper, output=output, inline=True)
    if output == "mlir":
        suffix = "mlir"
    else:
        suffix = "v"
    assert m.testing.check_files_equal(
        __file__, f"build/{basename}.{suffix}", f"gold/{basename}.{suffix}")
