module no_outputs(
  input I
);

endmodule

module simple_side_effect_instance(
  input  I,
  output O
);

  no_outputs no_outputs_inst0 (
    .I (I)
  );
  assign O = I;
endmodule

