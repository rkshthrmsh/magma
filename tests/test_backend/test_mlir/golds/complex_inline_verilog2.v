module complex_inline_verilog2(
  input  [11:0] I,
  input         CLK,
  output [11:0] O
);

  reg [11:0] Register_inst0;
  always_ff @(posedge CLK)
    Register_inst0 <= I;
  initial
    Register_inst0 = 12'h0;
  assert property (@(posedge CLK) I[0] |-> ##1 Register_inst0[0]);
  assert property (@(posedge CLK) I[1] |-> ##1 Register_inst0[1]);
  assert property (@(posedge CLK) I[2] |-> ##1 Register_inst0[2]);
  assert property (@(posedge CLK) I[3] |-> ##1 Register_inst0[3]);
  assert property (@(posedge CLK) I[4] |-> ##1 Register_inst0[4]);
  assert property (@(posedge CLK) I[5] |-> ##1 Register_inst0[5]);
  assert property (@(posedge CLK) I[6] |-> ##1 Register_inst0[6]);
  assert property (@(posedge CLK) I[7] |-> ##1 Register_inst0[7]);
  assert property (@(posedge CLK) I[8] |-> ##1 Register_inst0[8]);
  assert property (@(posedge CLK) I[9] |-> ##1 Register_inst0[9]);
  assert property (@(posedge CLK) I[10] |-> ##1 Register_inst0[10]);
  assert property (@(posedge CLK) I[11] |-> ##1 Register_inst0[11]);
  // A fun{k}y comment with I
  assign O = Register_inst0;
endmodule

