module aggregate_mux_wrapper(
  input  struct packed {logic [7:0] x; logic y; } a,
  input                                           s,
  output struct packed {logic [7:0] x; logic y; } y
);

  wire struct packed {logic [7:0] x; logic y; }      _GEN = '{x: (~a.x), y: (~a.y)};
  wire struct packed {logic [7:0] x; logic y; }[1:0] _GEN_0 = {{_GEN}, {a}};
  assign y = _GEN_0[s];
endmodule

