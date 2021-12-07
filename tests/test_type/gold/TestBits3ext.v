module mantle_concatNArrT__Ns33__t_childBitIn (
    input [2:0] in0,
    input [2:0] in1,
    output [5:0] out
);
assign out = {in1[2],in1[1],in1[0],in0[2],in0[1],in0[0]};
endmodule

module coreir_const #(
    parameter width = 1,
    parameter value = 1
) (
    output [width-1:0] out
);
  assign out = value;
endmodule

module TestExt (
    input [2:0] I,
    output [5:0] O
);
wire [5:0] ConcatN_inst0_out;
wire [2:0] const_0_3_out;
mantle_concatNArrT__Ns33__t_childBitIn ConcatN_inst0 (
    .in0(I),
    .in1(const_0_3_out),
    .out(ConcatN_inst0_out)
);
coreir_const #(
    .value(3'h0),
    .width(3)
) const_0_3 (
    .out(const_0_3_out)
);
assign O = ConcatN_inst0_out;
endmodule

