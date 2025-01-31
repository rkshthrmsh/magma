module simple_reduction(
  input  [7:0] I0,
               I1,
               I2,
  output       O0,
               O1,
               O2
);

  assign O0 = &I0;
  assign O1 = |I1;
  assign O2 = ^I2;
endmodule

