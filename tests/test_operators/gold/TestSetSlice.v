module mantle_concatNArrT__Ns33__t_childBitIn (
    input [2:0] in0,
    input [2:0] in1,
    output [5:0] out
);
assign out = {in1[2],in1[1],in1[0],in0[2],in0[1],in0[0]};
endmodule

module Mux2xBit (
    input I0,
    input I1,
    input S,
    output O
);
reg [0:0] coreir_commonlib_mux2x1_inst0_out;
always @(*) begin
if (S == 0) begin
    coreir_commonlib_mux2x1_inst0_out = I0;
end else begin
    coreir_commonlib_mux2x1_inst0_out = I1;
end
end

assign O = coreir_commonlib_mux2x1_inst0_out[0];
endmodule

module TestSetSlice (
    input [5:0] I,
    input [1:0] x,
    output [11:0] O
);
wire [5:0] ConcatN_inst0_out;
wire [5:0] ConcatN_inst1_out;
wire [5:0] ConcatN_inst10_out;
wire [5:0] ConcatN_inst11_out;
wire [5:0] ConcatN_inst2_out;
wire [5:0] ConcatN_inst3_out;
wire [5:0] ConcatN_inst4_out;
wire [5:0] ConcatN_inst5_out;
wire [5:0] ConcatN_inst6_out;
wire [5:0] ConcatN_inst7_out;
wire [5:0] ConcatN_inst8_out;
wire [5:0] ConcatN_inst9_out;
wire [1:0] Const_inst1_out;
wire Mux2xBit_inst0_O;
wire Mux2xBit_inst1_O;
wire Mux2xBit_inst10_O;
wire Mux2xBit_inst11_O;
wire Mux2xBit_inst2_O;
wire Mux2xBit_inst3_O;
wire Mux2xBit_inst4_O;
wire Mux2xBit_inst5_O;
wire Mux2xBit_inst6_O;
wire Mux2xBit_inst7_O;
wire Mux2xBit_inst8_O;
wire Mux2xBit_inst9_O;
wire magma_Bit_and_inst0_out;
wire magma_Bit_and_inst10_out;
wire magma_Bit_and_inst11_out;
wire magma_Bit_and_inst12_out;
wire magma_Bit_and_inst13_out;
wire magma_Bit_and_inst2_out;
wire magma_Bit_and_inst4_out;
wire magma_Bit_and_inst5_out;
wire magma_Bit_and_inst6_out;
wire magma_Bit_and_inst7_out;
wire magma_Bit_and_inst8_out;
wire magma_Bit_and_inst9_out;
wire [5:0] magma_Bits_6_lshr_inst0_out;
wire [5:0] magma_Bits_6_lshr_inst1_out;
wire [5:0] magma_Bits_6_lshr_inst10_out;
wire [5:0] magma_Bits_6_lshr_inst11_out;
wire [5:0] magma_Bits_6_lshr_inst2_out;
wire [5:0] magma_Bits_6_lshr_inst3_out;
wire [5:0] magma_Bits_6_lshr_inst4_out;
wire [5:0] magma_Bits_6_lshr_inst5_out;
wire [5:0] magma_Bits_6_lshr_inst6_out;
wire [5:0] magma_Bits_6_lshr_inst7_out;
wire [5:0] magma_Bits_6_lshr_inst8_out;
wire [5:0] magma_Bits_6_lshr_inst9_out;
wire [3:0] magma_UInt_4_sub_inst0_out;
wire [3:0] magma_UInt_4_sub_inst10_out;
wire [3:0] magma_UInt_4_sub_inst12_out;
wire [3:0] magma_UInt_4_sub_inst14_out;
wire [3:0] magma_UInt_4_sub_inst16_out;
wire [3:0] magma_UInt_4_sub_inst18_out;
wire [3:0] magma_UInt_4_sub_inst2_out;
wire [3:0] magma_UInt_4_sub_inst20_out;
wire [3:0] magma_UInt_4_sub_inst22_out;
wire [3:0] magma_UInt_4_sub_inst4_out;
wire [3:0] magma_UInt_4_sub_inst6_out;
wire [3:0] magma_UInt_4_sub_inst8_out;
mantle_concatNArrT__Ns33__t_childBitIn ConcatN_inst0 (
    .in0(magma_UInt_4_sub_inst0_out[2:0]),
    .in1(3'h0),
    .out(ConcatN_inst0_out)
);
mantle_concatNArrT__Ns33__t_childBitIn ConcatN_inst1 (
    .in0(magma_UInt_4_sub_inst2_out[2:0]),
    .in1(3'h0),
    .out(ConcatN_inst1_out)
);
mantle_concatNArrT__Ns33__t_childBitIn ConcatN_inst10 (
    .in0(magma_UInt_4_sub_inst20_out[2:0]),
    .in1(3'h0),
    .out(ConcatN_inst10_out)
);
mantle_concatNArrT__Ns33__t_childBitIn ConcatN_inst11 (
    .in0(magma_UInt_4_sub_inst22_out[2:0]),
    .in1(3'h0),
    .out(ConcatN_inst11_out)
);
mantle_concatNArrT__Ns33__t_childBitIn ConcatN_inst2 (
    .in0(magma_UInt_4_sub_inst4_out[2:0]),
    .in1(3'h0),
    .out(ConcatN_inst2_out)
);
mantle_concatNArrT__Ns33__t_childBitIn ConcatN_inst3 (
    .in0(magma_UInt_4_sub_inst6_out[2:0]),
    .in1(3'h0),
    .out(ConcatN_inst3_out)
);
mantle_concatNArrT__Ns33__t_childBitIn ConcatN_inst4 (
    .in0(magma_UInt_4_sub_inst8_out[2:0]),
    .in1(3'h0),
    .out(ConcatN_inst4_out)
);
mantle_concatNArrT__Ns33__t_childBitIn ConcatN_inst5 (
    .in0(magma_UInt_4_sub_inst10_out[2:0]),
    .in1(3'h0),
    .out(ConcatN_inst5_out)
);
mantle_concatNArrT__Ns33__t_childBitIn ConcatN_inst6 (
    .in0(magma_UInt_4_sub_inst12_out[2:0]),
    .in1(3'h0),
    .out(ConcatN_inst6_out)
);
mantle_concatNArrT__Ns33__t_childBitIn ConcatN_inst7 (
    .in0(magma_UInt_4_sub_inst14_out[2:0]),
    .in1(3'h0),
    .out(ConcatN_inst7_out)
);
mantle_concatNArrT__Ns33__t_childBitIn ConcatN_inst8 (
    .in0(magma_UInt_4_sub_inst16_out[2:0]),
    .in1(3'h0),
    .out(ConcatN_inst8_out)
);
mantle_concatNArrT__Ns33__t_childBitIn ConcatN_inst9 (
    .in0(magma_UInt_4_sub_inst18_out[2:0]),
    .in1(3'h0),
    .out(ConcatN_inst9_out)
);
assign Const_inst1_out = 2'h0;
Mux2xBit Mux2xBit_inst0 (
    .I0(1'b1),
    .I1(magma_Bits_6_lshr_inst0_out[0]),
    .S(magma_Bit_and_inst0_out),
    .O(Mux2xBit_inst0_O)
);
Mux2xBit Mux2xBit_inst1 (
    .I0(1'b1),
    .I1(magma_Bits_6_lshr_inst1_out[0]),
    .S(magma_Bit_and_inst2_out),
    .O(Mux2xBit_inst1_O)
);
Mux2xBit Mux2xBit_inst10 (
    .I0(1'b1),
    .I1(magma_Bits_6_lshr_inst10_out[0]),
    .S(magma_Bit_and_inst12_out),
    .O(Mux2xBit_inst10_O)
);
Mux2xBit Mux2xBit_inst11 (
    .I0(1'b1),
    .I1(magma_Bits_6_lshr_inst11_out[0]),
    .S(magma_Bit_and_inst13_out),
    .O(Mux2xBit_inst11_O)
);
Mux2xBit Mux2xBit_inst2 (
    .I0(1'b1),
    .I1(magma_Bits_6_lshr_inst2_out[0]),
    .S(magma_Bit_and_inst4_out),
    .O(Mux2xBit_inst2_O)
);
Mux2xBit Mux2xBit_inst3 (
    .I0(1'b1),
    .I1(magma_Bits_6_lshr_inst3_out[0]),
    .S(magma_Bit_and_inst5_out),
    .O(Mux2xBit_inst3_O)
);
Mux2xBit Mux2xBit_inst4 (
    .I0(1'b1),
    .I1(magma_Bits_6_lshr_inst4_out[0]),
    .S(magma_Bit_and_inst6_out),
    .O(Mux2xBit_inst4_O)
);
Mux2xBit Mux2xBit_inst5 (
    .I0(1'b1),
    .I1(magma_Bits_6_lshr_inst5_out[0]),
    .S(magma_Bit_and_inst7_out),
    .O(Mux2xBit_inst5_O)
);
Mux2xBit Mux2xBit_inst6 (
    .I0(1'b1),
    .I1(magma_Bits_6_lshr_inst6_out[0]),
    .S(magma_Bit_and_inst8_out),
    .O(Mux2xBit_inst6_O)
);
Mux2xBit Mux2xBit_inst7 (
    .I0(1'b1),
    .I1(magma_Bits_6_lshr_inst7_out[0]),
    .S(magma_Bit_and_inst9_out),
    .O(Mux2xBit_inst7_O)
);
Mux2xBit Mux2xBit_inst8 (
    .I0(1'b1),
    .I1(magma_Bits_6_lshr_inst8_out[0]),
    .S(magma_Bit_and_inst10_out),
    .O(Mux2xBit_inst8_O)
);
Mux2xBit Mux2xBit_inst9 (
    .I0(1'b1),
    .I1(magma_Bits_6_lshr_inst9_out[0]),
    .S(magma_Bit_and_inst11_out),
    .O(Mux2xBit_inst9_O)
);
assign magma_Bit_and_inst0_out = 1'b1 & (({Const_inst1_out[1:0],x[1:0]}) <= 4'h0);
assign magma_Bit_and_inst10_out = 1'b1 & ((4'((4'(({Const_inst1_out[1:0],x[1:0]}) + 4'h6)) - 4'h1)) >= 4'h8);
assign magma_Bit_and_inst11_out = 1'b1 & ((4'((4'(({Const_inst1_out[1:0],x[1:0]}) + 4'h6)) - 4'h1)) >= 4'h9);
assign magma_Bit_and_inst12_out = 1'b1 & ((4'((4'(({Const_inst1_out[1:0],x[1:0]}) + 4'h6)) - 4'h1)) >= 4'ha);
assign magma_Bit_and_inst13_out = 1'b1 & ((4'((4'(({Const_inst1_out[1:0],x[1:0]}) + 4'h6)) - 4'h1)) >= 4'hb);
assign magma_Bit_and_inst2_out = (1'b1 & (({Const_inst1_out[1:0],x[1:0]}) <= 4'h1)) & ((4'((4'(({Const_inst1_out[1:0],x[1:0]}) + 4'h6)) - 4'h1)) >= 4'h1);
assign magma_Bit_and_inst4_out = (1'b1 & (({Const_inst1_out[1:0],x[1:0]}) <= 4'h2)) & ((4'((4'(({Const_inst1_out[1:0],x[1:0]}) + 4'h6)) - 4'h1)) >= 4'h2);
assign magma_Bit_and_inst5_out = 1'b1 & ((4'((4'(({Const_inst1_out[1:0],x[1:0]}) + 4'h6)) - 4'h1)) >= 4'h3);
assign magma_Bit_and_inst6_out = 1'b1 & ((4'((4'(({Const_inst1_out[1:0],x[1:0]}) + 4'h6)) - 4'h1)) >= 4'h4);
assign magma_Bit_and_inst7_out = 1'b1 & ((4'((4'(({Const_inst1_out[1:0],x[1:0]}) + 4'h6)) - 4'h1)) >= 4'h5);
assign magma_Bit_and_inst8_out = 1'b1 & ((4'((4'(({Const_inst1_out[1:0],x[1:0]}) + 4'h6)) - 4'h1)) >= 4'h6);
assign magma_Bit_and_inst9_out = 1'b1 & ((4'((4'(({Const_inst1_out[1:0],x[1:0]}) + 4'h6)) - 4'h1)) >= 4'h7);
assign magma_Bits_6_lshr_inst0_out = I >> ConcatN_inst0_out;
assign magma_Bits_6_lshr_inst1_out = I >> ConcatN_inst1_out;
assign magma_Bits_6_lshr_inst10_out = I >> ConcatN_inst10_out;
assign magma_Bits_6_lshr_inst11_out = I >> ConcatN_inst11_out;
assign magma_Bits_6_lshr_inst2_out = I >> ConcatN_inst2_out;
assign magma_Bits_6_lshr_inst3_out = I >> ConcatN_inst3_out;
assign magma_Bits_6_lshr_inst4_out = I >> ConcatN_inst4_out;
assign magma_Bits_6_lshr_inst5_out = I >> ConcatN_inst5_out;
assign magma_Bits_6_lshr_inst6_out = I >> ConcatN_inst6_out;
assign magma_Bits_6_lshr_inst7_out = I >> ConcatN_inst7_out;
assign magma_Bits_6_lshr_inst8_out = I >> ConcatN_inst8_out;
assign magma_Bits_6_lshr_inst9_out = I >> ConcatN_inst9_out;
assign magma_UInt_4_sub_inst0_out = 4'(4'h0 - ({Const_inst1_out[1:0],x[1:0]}));
assign magma_UInt_4_sub_inst10_out = 4'(4'h5 - ({Const_inst1_out[1:0],x[1:0]}));
assign magma_UInt_4_sub_inst12_out = 4'(4'h6 - ({Const_inst1_out[1:0],x[1:0]}));
assign magma_UInt_4_sub_inst14_out = 4'(4'h7 - ({Const_inst1_out[1:0],x[1:0]}));
assign magma_UInt_4_sub_inst16_out = 4'(4'h8 - ({Const_inst1_out[1:0],x[1:0]}));
assign magma_UInt_4_sub_inst18_out = 4'(4'h9 - ({Const_inst1_out[1:0],x[1:0]}));
assign magma_UInt_4_sub_inst2_out = 4'(4'h1 - ({Const_inst1_out[1:0],x[1:0]}));
assign magma_UInt_4_sub_inst20_out = 4'(4'ha - ({Const_inst1_out[1:0],x[1:0]}));
assign magma_UInt_4_sub_inst22_out = 4'(4'hb - ({Const_inst1_out[1:0],x[1:0]}));
assign magma_UInt_4_sub_inst4_out = 4'(4'h2 - ({Const_inst1_out[1:0],x[1:0]}));
assign magma_UInt_4_sub_inst6_out = 4'(4'h3 - ({Const_inst1_out[1:0],x[1:0]}));
assign magma_UInt_4_sub_inst8_out = 4'(4'h4 - ({Const_inst1_out[1:0],x[1:0]}));
assign O = {Mux2xBit_inst11_O,Mux2xBit_inst10_O,Mux2xBit_inst9_O,Mux2xBit_inst8_O,Mux2xBit_inst7_O,Mux2xBit_inst6_O,Mux2xBit_inst5_O,Mux2xBit_inst4_O,Mux2xBit_inst3_O,Mux2xBit_inst2_O,Mux2xBit_inst1_O,Mux2xBit_inst0_O};
endmodule

