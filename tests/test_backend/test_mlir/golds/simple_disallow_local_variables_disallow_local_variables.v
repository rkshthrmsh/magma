module simple_disallow_local_variables(
  input  [1:0] x,
  input        s,
  output [1:0] O
);

  reg [1:0] _GEN;
  always_comb begin
    if (s)
      _GEN = ~x;
    else
      _GEN = x;
  end // always_comb
  reg       _GEN_0;
  reg       _GEN_1;
  always_comb begin
    if (~s) begin
      _GEN_0 = _GEN[1];
      _GEN_1 = _GEN[0];
    end
    else begin
      _GEN_0 = _GEN[0];
      _GEN_1 = _GEN[1];
    end
  end // always_comb
  assign O = {_GEN_1, _GEN_0};
endmodule

