module complex_bind_asserts(
  input I_I,
        O,
        CLK,
        I0
);

  assert property (@(posedge CLK) I_I |-> ##1 O);assert property (I_I |-> I0;
endmodule

module complex_bind(
  input  I_I,
         CLK,
  output O
);

  reg Register_inst0;
  always_ff @(posedge CLK)
    Register_inst0 <= I_I;
  initial
    Register_inst0 = 1'h0;
  assign O = Register_inst0;
endmodule


// ----- 8< ----- FILE "bindfile.sv" ----- 8< -----

bind complex_bind complex_bind_asserts complex_bind_asserts_inst (
  .I_I (I_I),
  .O   (Register_inst0),
  .CLK (CLK),
  .I0  (~I_I)
);
