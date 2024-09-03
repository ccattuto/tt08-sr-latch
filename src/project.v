/*
 * Copyright (c) 2024 Ciro Cattuto <ciro.cattuto@gmail.com>
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_cattuto_sr_latch (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

  // All output pins must be assigned. If not used, assign to 0.
  assign uo_out[7:1] = 0;
  assign uio_out = 0;
  assign uio_oe  = 0;

  // List all unused inputs to prevent warnings
  wire _unused = &{ena, clk, rst_n, 1'b0};

  wire sr_in = ui_in[0];
  wire sr_out = uo_out[0];

  parameter SR_LEN = 128;  // Default length of the shift register

  // Internal signals for the two-phase clock generation
  reg clk1;
  reg clk2;

  // Two-phase clock generation
  always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      clk1 <= 0;
      clk2 <= 0;
    end else begin
      clk1 <= ~clk1;
      clk2 <= clk1; // clk2 is the inverted version of clk1, offset by half clock cycle
    end
  end

  // Internal signals for the latches
  wire [SR_LEN-1:0] q;

  // Generate shift register with alternating clock phases
  genvar i;
  generate
    for (i = 0; i < SR_LEN; i = i + 1) begin : shift_reg
      if (i == 0) begin
        // First latch takes input from sr_in
        d_latch latch (.d(sr_in), .clk((i % 2) ? clk2 : clk1), .rst_n(rst_n), .q(q[i]));
      end else begin
        // Subsequent latches take input from previous latch
        d_latch latch (.d(q[i-1]), .clk((i % 2) ? clk2 : clk1), .rst_n(rst_n), .q(q[i]));
      end
    end
  endgenerate

  // Output assignment
  assign sr_out = q[SR_LEN-1];    // Output the last latch value

endmodule
