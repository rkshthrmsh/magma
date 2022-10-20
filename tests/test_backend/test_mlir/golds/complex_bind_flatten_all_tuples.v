// Generated by CIRCT circtorg-0.0.0-658-g0d82b4bb2
module complex_bind_asserts(
  input I_I,
        O,
        CLK,
        I0);

  wire _magma_inline_wire0 = O;
  wire _magma_inline_wire1 = I_I;
  wire _magma_inline_wire2 = I0;
  assert property (@(posedge CLK) _magma_inline_wire1 |-> ##1 _magma_inline_wire0);assert property (_magma_inline_wire1 |-> _magma_inline_wire2;
endmodule

module complex_bind(
  input  I_I,
         CLK,
  output O);

  wire _complex_bind_asserts_inst_I0;
  reg  Register_inst0;
  always_ff @(posedge CLK)
    Register_inst0 <= I_I;
  initial
    Register_inst0 = 1'h0;
  assign _complex_bind_asserts_inst_I0 = ~I_I;
  /* This instance is elsewhere emitted as a bind statement.
    complex_bind_asserts complex_bind_asserts_inst (
      .I_I (I_I),
      .O   (Register_inst0),
      .CLK (CLK),
      .I0  (_complex_bind_asserts_inst_I0)
    );
  */
  assign O = Register_inst0;
endmodule


// ----- 8< ----- FILE "bindfile" ----- 8< -----

bind complex_bind complex_bind_asserts complex_bind_asserts_inst (
  .I_I (I_I),
  .O   (Register_inst0),
  .CLK (CLK),
  .I0  (_complex_bind_asserts_inst_I0)
);
