// Module `Foo` defined externally
module coreir_wire #(parameter width = 1) (input [width-1:0] in, output [width-1:0] out);
  assign out = in;
endmodule

module Main (input [4:0] I__0, input I__1, output [4:0] O__0, output O__1);
wire [4:0] Foo_inst0_O__0;
wire Foo_inst0_O__1;
wire [5:0] wire_Foo_inst0_O_x_out;
wire [5:0] wire_I_Foo_inst0_I_out;
wire [5:0] wire_x_O_out;
Foo Foo_inst0(.I__0({wire_I_Foo_inst0_I_out[4],wire_I_Foo_inst0_I_out[3],wire_I_Foo_inst0_I_out[2],wire_I_Foo_inst0_I_out[1],wire_I_Foo_inst0_I_out[0]}), .I__1(wire_I_Foo_inst0_I_out[5]), .O__0(Foo_inst0_O__0), .O__1(Foo_inst0_O__1));
coreir_wire #(.width(6)) wire_Foo_inst0_O_x(.in({Foo_inst0_O__1,Foo_inst0_O__0[4],Foo_inst0_O__0[3],Foo_inst0_O__0[2],Foo_inst0_O__0[1],Foo_inst0_O__0[0]}), .out(wire_Foo_inst0_O_x_out));
coreir_wire #(.width(6)) wire_I_Foo_inst0_I(.in({I__1,I__0[4],I__0[3],I__0[2],I__0[1],I__0[0]}), .out(wire_I_Foo_inst0_I_out));
coreir_wire #(.width(6)) wire_x_O(.in(wire_Foo_inst0_O_x_out), .out(wire_x_O_out));
assign O__0 = {wire_x_O_out[4],wire_x_O_out[3],wire_x_O_out[2],wire_x_O_out[1],wire_x_O_out[0]};
assign O__1 = wire_x_O_out[5];
endmodule

