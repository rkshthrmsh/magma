module TestRepeat (input [0:0] I, output [6:0] O);
assign O = {I[0],I[0],I[0],I[0],I[0],I[0],I[0]};
endmodule

