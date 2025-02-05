module xmr_bind_grandchild(
  input  [15:0] a,
  output [15:0] y
);

  assign y = a;
endmodule

module xmr_bind_child(
  input  [15:0] a,
  output [15:0] y
);

  xmr_bind_grandchild xmr_bind_grandchild_inst0 (
    .a (a),
    .y (y)
  );
endmodule

module xmr_bind_asserts(
  input [15:0] a,
               y,
               other
);

  assert property (other == 0);
endmodule

module xmr_bind(
  input  [15:0] a,
  output [15:0] y
);

  wire [15:0] _xmr_bind_child_inst0_y;
  xmr_bind_child xmr_bind_child_inst0 (
    .a (a),
    .y (_xmr_bind_child_inst0_y)
  );
  assign y = _xmr_bind_child_inst0_y;
endmodule


// ----- 8< ----- FILE "bindfile.sv" ----- 8< -----

bind xmr_bind xmr_bind_asserts xmr_bind_asserts_inst (
  .a     (a),
  .y     (_xmr_bind_child_inst0_y),
  .other (xmr_bind_child_inst0.xmr_bind_grandchild_inst0.y)
);
