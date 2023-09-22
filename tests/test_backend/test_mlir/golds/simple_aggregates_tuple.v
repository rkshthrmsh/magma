module simple_aggregates_tuple(
  input  struct packed {logic [7:0] _0; logic [7:0] _1; } a,
  output struct packed {logic [7:0] _0; logic [7:0] _1; } y
);

  assign y = '{_0: (~a._0), _1: (~a._1)};
endmodule

