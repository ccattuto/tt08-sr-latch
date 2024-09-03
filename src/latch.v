// D latch module
module d_latch (
    input  wire d,
    input  wire clk,
    input  wire rst_n,
    output reg q
);

  always @ (clk or negedge rst_n) begin
    if (!rst_n)
      q <= 0;
    else if (clk)
      q <= d;
  end

endmodule
