module LUT(
  input  [1:0] I,
  output [7:0] O
);

  wire [3:0] _GEN = {1'h1, 1'h0, 1'h0, 1'h1};
  wire [3:0] _GEN_0 = {1'h1, 1'h1, 1'h1, 1'h0};
  wire [3:0] _GEN_1 = {1'h0, 1'h1, 1'h0, 1'h1};
  wire [3:0] _GEN_2 = {1'h1, 1'h1, 1'h0, 1'h1};
  wire [3:0] _GEN_3 = {1'h1, 1'h0, 1'h1, 1'h0};
  assign O = {1'h1, _GEN[I], _GEN_0[I], _GEN_1[I], 2'h3, _GEN_2[I], _GEN_3[I]};
endmodule

module simple_lut(
  input  [1:0] a,
  output [7:0] y
);

  LUT LUT_inst0 (
    .I (a),
    .O (y)
  );
endmodule

