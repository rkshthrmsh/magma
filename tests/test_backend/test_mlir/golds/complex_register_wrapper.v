module complex_register_wrapper(
  input  struct packed {logic [7:0] x; logic y; }                                          a,
  input  [5:0][15:0]                                                                       b,
  input                                                                                    CLK,
                                                                                           CE,
                                                                                           ASYNCRESET,
  output struct packed {struct packed {logic [7:0] x; logic y; } u; logic [5:0][15:0] v; } y
);

     struct packed {logic [7:0] x; logic y; } Register_inst0;
  always_ff @(posedge CLK or posedge ASYNCRESET) begin
    if (ASYNCRESET)
      Register_inst0 <= '{x: 8'hA, y: 1'h1};
    else begin
      if (CE)
        Register_inst0 <= a;
    end
  end // always_ff @(posedge or posedge)
  reg [5:0][15:0]                              Register_inst1;
  reg [7:0]                                    Register_inst2;
  always_ff @(posedge CLK) begin
    Register_inst1 <= b;
    if (CE)
      Register_inst2 <= a.x;
  end // always_ff @(posedge)
  initial begin
    Register_inst0 = '{x: 8'hA, y: 1'h1};
    Register_inst1 = {16'h0, 16'h2, 16'h4, 16'h6, 16'h8, 16'hA};
    Register_inst2 = 8'h0;
  end // initial
  assign y = '{u: Register_inst0, v: Register_inst1};
endmodule

