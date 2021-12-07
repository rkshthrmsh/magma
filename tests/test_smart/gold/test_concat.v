module mantle_concatNArrT__Ns44__t_childBitIn (
    input [3:0] in0,
    input [3:0] in1,
    output [7:0] out
);
assign out = {in1[3],in1[2],in1[1],in1[0],in0[3],in0[2],in0[1],in0[0]};
endmodule

module _Test (
    input [7:0] I0,
    input [3:0] I1,
    input [9:0] I2,
    output [3:0] O1,
    output [15:0] O2
);
wire [7:0] ConcatN_inst0_out;
wire [7:0] ConcatN_inst1_out;
wire [7:0] magma_UInt_8_add_inst0_out;
mantle_concatNArrT__Ns44__t_childBitIn ConcatN_inst0 (
    .in0(I1),
    .in1(4'h0),
    .out(ConcatN_inst0_out)
);
mantle_concatNArrT__Ns44__t_childBitIn ConcatN_inst1 (
    .in0(I1),
    .in1(4'h0),
    .out(ConcatN_inst1_out)
);
assign magma_UInt_8_add_inst0_out = 8'(I0 + ConcatN_inst0_out);
assign O1 = magma_UInt_8_add_inst0_out[3:0];
assign O2 = {I2[7:0],8'(I0 + ConcatN_inst1_out)};
endmodule

