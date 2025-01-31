module TestLog(
  input  I,
         CLK,
         CE,
  output O
);

  reg ff;
  always_ff @(posedge CLK) begin
    if (CE)
      ff <= I;
  end // always_ff @(posedge)
  initial
    ff = 1'h0;

  `ifndef MAGMA_LOG_LEVEL
      `define MAGMA_LOG_LEVEL 1
  `endif
  always @(posedge CLK) begin
      if ((`MAGMA_LOG_LEVEL <= 0) && (CE)) $display("[DEBUG] ff.O=%d, ff.I=%d", ff, I);
  end
  always @(posedge CLK) begin
      if ((`MAGMA_LOG_LEVEL <= 1) && (CE)) $display("[INFO] ff.O=%d, ff.I=%d", ff, I);
  end
  always @(posedge CLK) begin
      if ((`MAGMA_LOG_LEVEL <= 2) && (CE)) $display("[WARNING] ff.O=%d, ff.I=%d", ff, I);
  end
  always @(posedge CLK) begin
      if ((`MAGMA_LOG_LEVEL <= 3) && (CE)) $display("[ERROR] ff.O=%d, ff.I=%d", ff, I);
  end
  assign O = ff;
endmodule

