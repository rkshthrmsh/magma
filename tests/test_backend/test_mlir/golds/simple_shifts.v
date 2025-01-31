module simple_shifts(
  input  [7:0] I00,
               I01,
               I10,
               I11,
               I20,
               I21,
  output [7:0] O0,
               O1,
               O2
);

  assign O0 = I00 << I01;
  assign O1 = I10 >> I11;
  assign O2 = $signed($signed(I20) >>> I21);
endmodule

