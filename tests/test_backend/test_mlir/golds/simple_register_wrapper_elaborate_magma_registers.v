module Register(
  input  [7:0] I,
  input        CLK,
  output [7:0] O
);

  reg [7:0] reg_P8_inst0;
  always_ff @(posedge CLK)
    reg_P8_inst0 <= I;
  initial
    reg_P8_inst0 = 8'h3;
  assign O = reg_P8_inst0;
endmodule

module simple_register_wrapper(
  input  [7:0] a,
  input        CLK,
  output [7:0] y
);

  Register reg0 (
    .I   (a),
    .CLK (CLK),
    .O   (y)
  );
endmodule

