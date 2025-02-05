module non_power_of_two_mux_wrapper(
  input  [7:0] a_x,
  input        a_y,
  input  [3:0] s,
  output [7:0] y_x,
  output       y_y
);

  wire [15:0][7:0] _GEN =
    {{~a_x},
     {~a_x},
     {~a_x},
     {~a_x},
     {~a_x},
     {~a_x},
     {~a_x},
     {~a_x},
     {~a_x},
     {~a_x},
     {~a_x},
     {~a_x},
     {~a_x},
     {~a_x},
     {~a_x},
     {a_x}};
  wire [15:0]      _GEN_0 =
    {{~a_y},
     {~a_y},
     {~a_y},
     {~a_y},
     {~a_y},
     {~a_y},
     {~a_y},
     {~a_y},
     {~a_y},
     {~a_y},
     {~a_y},
     {~a_y},
     {~a_y},
     {~a_y},
     {~a_y},
     {a_y}};
  assign y_x = _GEN[s];
  assign y_y = _GEN_0[s];
endmodule

