module complex_mixed_direction_ports(
  input  [7:0] a_0_x,
               a_1_x,
               a_2_x,
               a_3_x,
               a_4_x,
               a_5_x,
               a_6_x,
               a_7_x,
               b_y,
  output [7:0] a_0_y,
               a_1_y,
               a_2_y,
               a_3_y,
               a_4_y,
               a_5_y,
               a_6_y,
               a_7_y,
               b_x
);

  assign a_0_y = 8'h0;
  assign a_1_y = b_y;
  assign a_2_y = 8'h0;
  assign a_3_y = 8'h0;
  assign a_4_y = 8'h0;
  assign a_5_y = 8'h0;
  assign a_6_y = 8'h0;
  assign a_7_y = 8'h0;
  assign b_x = a_1_x;
endmodule

