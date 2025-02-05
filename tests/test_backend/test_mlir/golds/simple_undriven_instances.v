module simple_comb(
  input  [15:0] a,
                b,
                c,
  output [15:0] y,
                z
);

  assign y = 16'hFFFF;
  assign z = 16'hFFFF;
endmodule

module simple_undriven_instances();
  wire [15:0] _GEN;
  wire [15:0] _GEN_0;
  wire [15:0] _GEN_1;
  wire [15:0] _GEN_2;
  wire [15:0] _GEN_3;
  wire [15:0] _GEN_4;
  simple_comb simple_comb_inst0 (
    .a (_GEN),
    .b (_GEN_0),
    .c (_GEN_1),
    .y (/* unused */),
    .z (/* unused */)
  );
  simple_comb simple_comb_inst1 (
    .a (_GEN_2),
    .b (_GEN_3),
    .c (_GEN_4),
    .y (/* unused */),
    .z (/* unused */)
  );
endmodule

