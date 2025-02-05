module simple_register_wrapper(
  input  [7:0] a,
  input        CLK,
  output [7:0] y
);

  reg [7:0] reg0;
  always_ff @(posedge CLK)
    reg0 <= a;
  assign y = reg0;
endmodule

