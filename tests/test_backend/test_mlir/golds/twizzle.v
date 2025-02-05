module twizzler(
  input  I0,
         I1,
         I2,
  output O0,
         O1,
         O2
);

  assign O0 = ~I1;
  assign O1 = ~I0;
  assign O2 = ~I2;
endmodule

module twizzle(
  input  I,
  output O
);

  wire _t1_O0;
  wire _t1_O1;
  wire _t0_O0;
  wire _t0_O1;
  wire _t0_O2;
  twizzler t0 (
    .I0 (I),
    .I1 (_t1_O0),
    .I2 (_t1_O1),
    .O0 (_t0_O0),
    .O1 (_t0_O1),
    .O2 (_t0_O2)
  );
  twizzler t1 (
    .I0 (_t0_O0),
    .I1 (_t0_O1),
    .I2 (_t0_O2),
    .O0 (_t1_O0),
    .O1 (_t1_O1),
    .O2 (O)
  );
endmodule

