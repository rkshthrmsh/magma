// Generated by CIRCT unknown git version
module Foo(	// <stdin>:1:1
  input  [1:0] I,
  input        S,
  output       O);

  reg O0_reg;	// <stdin>:4:10

  always_comb begin	// <stdin>:5:5
    if (S)	// <stdin>:6:9
      O0_reg = I[0];	// <stdin>:2:10, :7:13
    else	// <stdin>:6:9
      O0_reg = I[1];	// <stdin>:3:10, :9:13
  end // always_comb
  assign O = O0_reg;	// <stdin>:12:10, :13:5
endmodule

