module coreir_reg #(
    parameter width = 1,
    parameter clk_posedge = 1,
    parameter init = 1
) (
    input clk,
    input [width-1:0] in,
    output [width-1:0] out
);
  reg [width-1:0] outReg=init;
  wire real_clk;
  assign real_clk = clk_posedge ? clk : ~clk;
  always @(posedge real_clk) begin
    outReg <= in;
  end
  assign out = outReg;
endmodule

module corebit_term (
    input in
);

endmodule

module corebit_or (
    input in0,
    input in1,
    output out
);
  assign out = in0 | in1;
endmodule

module Register (
    input I,
    output O,
    input CLK
);
wire [0:0] reg_P1_inst0_out;
coreir_reg #(
    .clk_posedge(1'b1),
    .init(1'h0),
    .width(1)
) reg_P1_inst0 (
    .clk(CLK),
    .in(I),
    .out(reg_P1_inst0_out)
);
assign O = reg_P1_inst0_out[0];
endmodule

module DebugModule (
    input port_0,
    input port_1,
    input port_2
);
wire magma_Bit_or_inst0_out;
wire reg_O;
corebit_or magma_Bit_or_inst0 (
    .in0(\reg _O),
    .in1(port_1),
    .out(magma_Bit_or_inst0_out)
);
Register reg (
    .I(magma_Bit_or_inst0_out),
    .O(reg_O),
    .CLK(port_0)
);
assert port_2;
assert ~\reg _O;
endmodule

module Top (
    input I,
    output O,
    input CLK
);
`ifdef DEBUG
DebugModule DebugModule (
    .port_0(CLK),
    .port_1(I),
    .port_2(I)
);
`endif
assign O = I;
endmodule

