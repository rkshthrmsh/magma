module non_power_of_two_mux_wrapper(
  input  struct packed {logic [7:0] x; logic y; } a,
  input  [3:0]                                    s,
  output struct packed {logic [7:0] x; logic y; } y
);

  wire struct packed {logic [7:0] x; logic y; }       _GEN = '{x: (~a.x), y: (~a.y)};
  wire struct packed {logic [7:0] x; logic y; }       _GEN_0 = '{x: (~a.x), y: (~a.y)};
  wire struct packed {logic [7:0] x; logic y; }       _GEN_1 = '{x: (~a.x), y: (~a.y)};
  wire struct packed {logic [7:0] x; logic y; }       _GEN_2 = '{x: (~a.x), y: (~a.y)};
  wire struct packed {logic [7:0] x; logic y; }       _GEN_3 = '{x: (~a.x), y: (~a.y)};
  wire struct packed {logic [7:0] x; logic y; }       _GEN_4 = '{x: (~a.x), y: (~a.y)};
  wire struct packed {logic [7:0] x; logic y; }       _GEN_5 = '{x: (~a.x), y: (~a.y)};
  wire struct packed {logic [7:0] x; logic y; }       _GEN_6 = '{x: (~a.x), y: (~a.y)};
  wire struct packed {logic [7:0] x; logic y; }       _GEN_7 = '{x: (~a.x), y: (~a.y)};
  wire struct packed {logic [7:0] x; logic y; }       _GEN_8 = '{x: (~a.x), y: (~a.y)};
  wire struct packed {logic [7:0] x; logic y; }       _GEN_9 = '{x: (~a.x), y: (~a.y)};
  wire struct packed {logic [7:0] x; logic y; }[11:0] _GEN_10 =
    {{_GEN_9},
     {_GEN_8},
     {_GEN_7},
     {_GEN_6},
     {_GEN_5},
     {_GEN_4},
     {_GEN_3},
     {_GEN_2},
     {_GEN_1},
     {_GEN_0},
     {_GEN},
     {a}};
  assign y = _GEN_10[s];
endmodule

