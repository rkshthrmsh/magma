module complex_register_wrapper(
  input  [7:0]       a_x,
  input              a_y,
  input  [5:0][15:0] b,
  input              CLK,
                     CE,
                     ASYNCRESET,
  output [7:0]       y_u_x,
  output             y_u_y,
  output [5:0][15:0] y_v
);

  reg [7:0]       Register_inst0;
  reg             Register_inst0_0;
  always_ff @(posedge CLK or posedge ASYNCRESET) begin
    if (ASYNCRESET) begin
      Register_inst0 <= 8'hA;
      Register_inst0_0 <= 1'h1;
    end
    else begin
      if (CE) begin
        Register_inst0 <= a_x;
        Register_inst0_0 <= a_y;
      end
    end
  end // always_ff @(posedge or posedge)
  reg [5:0][15:0] Register_inst1;
  reg [7:0]       Register_inst2;
  always_ff @(posedge CLK) begin
    Register_inst1 <= b;
    if (CE)
      Register_inst2 <= a_x;
  end // always_ff @(posedge)
  initial begin
    Register_inst0 = 8'hA;
    Register_inst0_0 = 1'h1;
    Register_inst1 = {16'h0, 16'h2, 16'h4, 16'h6, 16'h8, 16'hA};
    Register_inst2 = 8'h0;
  end // initial
  assign y_u_x = Register_inst0;
  assign y_u_y = Register_inst0_0;
  assign y_v = Register_inst1;
endmodule

