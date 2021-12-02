// Module `Buf` defined externally
module coreir_const #(
    parameter width = 1,
    parameter value = 1
) (
    output [width-1:0] out
);
  assign out = value;
endmodule

module main (
    output [0:0] O
);
wire [0:0] Buf_inst0_O;
wire [0:0] Const_inst0_out;
Buf Buf_inst0 (
    .I(Const_inst0_out),
    .O(Buf_inst0_O)
);
coreir_const #(
    .value(1'h1),
    .width(1)
) Const_inst0 (
    .out(Const_inst0_out)
);
assign O = Buf_inst0_O;
endmodule

