// external module simple_decl

module simple_decl_external(
  input  I,
  output O
);

  simple_decl simple_decl_inst0 (
    .I (I),
    .O (O)
  );
endmodule

