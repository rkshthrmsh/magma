module Register(
  input  struct packed {logic [7:0] x; logic y; } I,
  input                                           CE,
                                                  CLK,
                                                  ASYNCRESET,
  output struct packed {logic [7:0] x; logic y; } O
);

  reg [8:0] reg_PR9_inst0;
  always_ff @(posedge CLK or posedge ASYNCRESET) begin
    if (ASYNCRESET)
      reg_PR9_inst0 <= 9'h10A;
    else begin
      automatic struct packed {logic [7:0] x; logic y; }      _GEN;
      automatic struct packed {logic [7:0] x; logic y; }[1:0] _GEN_0;
      _GEN = '{x: (reg_PR9_inst0[7:0]), y: (reg_PR9_inst0[8])};
      _GEN_0 = {{I}, {_GEN}};
      reg_PR9_inst0 <= {_GEN_0[CE].y, _GEN_0[CE].x};
    end
  end // always_ff @(posedge or posedge)
  initial
    reg_PR9_inst0 = 9'h10A;
  assign O = '{x: (reg_PR9_inst0[7:0]), y: (reg_PR9_inst0[8])};
endmodule

module Register_unq1(
  input  [5:0][15:0] I,
  input              CLK,
  output [5:0][15:0] O
);

  reg [95:0] reg_P96_inst0;
  always_ff @(posedge CLK)
    reg_P96_inst0 <= /*cast(bit[95:0])*/I;
  initial
    reg_P96_inst0 = 96'hA00080006000400020000;
  assign O =
    {{reg_P96_inst0[95:80]},
     {reg_P96_inst0[79:64]},
     {reg_P96_inst0[63:48]},
     {reg_P96_inst0[47:32]},
     {reg_P96_inst0[31:16]},
     {reg_P96_inst0[15:0]}};
endmodule

module Register_unq2(
  input  [7:0] I,
  input        CE,
               CLK,
  output [7:0] O
);

  reg [7:0] reg_P8_inst0;
  always_ff @(posedge CLK) begin
    automatic logic [1:0][7:0] _GEN;
    _GEN = {{I}, {reg_P8_inst0}};
    reg_P8_inst0 <= _GEN[CE];
  end // always_ff @(posedge)
  initial
    reg_P8_inst0 = 8'h0;
  assign O = reg_P8_inst0;
endmodule

module complex_register_wrapper(
  input  struct packed {logic [7:0] x; logic y; }                                          a,
  input  [5:0][15:0]                                                                       b,
  input                                                                                    CLK,
                                                                                           CE,
                                                                                           ASYNCRESET,
  output struct packed {struct packed {logic [7:0] x; logic y; } u; logic [5:0][15:0] v; } y
);

  wire [5:0][15:0]                              _Register_inst1_O;
  wire struct packed {logic [7:0] x; logic y; } _Register_inst0_O;
  Register Register_inst0 (
    .I          (a),
    .CE         (CE),
    .CLK        (CLK),
    .ASYNCRESET (ASYNCRESET),
    .O          (_Register_inst0_O)
  );
  Register_unq1 Register_inst1 (
    .I   (b),
    .CLK (CLK),
    .O   (_Register_inst1_O)
  );
  Register_unq2 Register_inst2 (
    .I   (a.x),
    .CE  (CE),
    .CLK (CLK),
    .O   (/* unused */)
  );
  assign y = '{u: _Register_inst0_O, v: _Register_inst1_O};
endmodule

