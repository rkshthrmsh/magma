// Generated by CIRCT firtool-1.48.0-34-g7018fb13b
module test_when_alwcomb_order_complex(
  input  [7:0] I,
  input  [1:0] S,
  output [7:0] O
);

  reg [7:0] _GEN;
  always_comb begin
    if (S[0]) begin
      _GEN = I;
      if (S[1])
        _GEN = ~I;
    end
    else if (^S)
      _GEN = 8'h0;
    else
      _GEN = ~I;
  end // always_comb
  reg [7:0] _GEN_0;
  always_comb begin
    _GEN_0 = _GEN;
    if (S[0]) begin
      if (S[1])
        _GEN_0 = _GEN & 8'hDE;
    end
    else if (^S) begin
    end
    else
      _GEN_0 = ~_GEN;
  end // always_comb
  assign O = _GEN_0;
endmodule

