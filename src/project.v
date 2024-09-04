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

  // List all unused signals to prevent warnings
  wire _unused = &{ena, clk, rst_n, ui_in[7:2], uio_in, dclk[0], 1'b0};

  wire sr_in, sr_out, shift;
  assign sr_in = ui_in[0];
  assign uo_out[0] = sr_out;

  wire nshift, shift2;
  (* dont_touch = "true" *) INV u_invA (.out(nshift), .in(ui_in[1]));
  (* dont_touch = "true" *) INV u_invB (.out(shift2), .in(nshift));

  assign shift = ui_in[1] ^ shift2;

  parameter SR_LEN = 512; // Default length of the shift register

  // Internal signals for the latches
  wire [SR_LEN-1:0] q;
  wire [SR_LEN-1:0] dclk;
  assign sr_out = q[SR_LEN-1];

  // reg [9:0] counter;
  // wire shift;
  // assign shift = counter[9];

  // always @(posedge clk or negedge rst_n) begin
  //   if (!rst_n) begin
  //     counter <= 0;
  //   end else begin
  //     counter <= counter + 1;
  //   end
  // end

  // Generate shift register with clock delay chain
  genvar i;
  generate
    for (i = 0; i < SR_LEN; i = i + 1) begin : shift_reg
      if (i == 0) begin
        // First latch takes input from sr_in
        d_latch latch (.d(sr_in), .clk(dclk[i+1]), .clkout(dclk[i]), .q(q[i]));
      end else if (i == SR_LEN-1) begin
        // Last latch takes input from the shift control signal
        d_latch latch (.d(q[i-1]), .clk(shift), .clkout(dclk[i]), .q(q[i]));
      end else begin
        // all other latches
        d_latch latch (.d(q[i-1]), .clk(dclk[i+1]), .clkout(dclk[i]), .q(q[i]));
      end
    end
  endgenerate

endmodule

module INV (
	input  wire in,
  output wire out
);

  sky130_fd_sc_hd__inv_2 cnt_bit_I (
    .A     (in),
    .Y     (out)
  );
endmodule

module d_latch (
    input  wire d,
    input  wire clk,
    output wire clkout,
    output reg q
);

  always @* begin
    if (clk) begin
      q = d; // latch the data
    end
    // q retains its previous value
  end

  wire clknext;
  (* dont_touch = "true" *) INV u_inv1 (.out(clknext), .in(clk));
  (* dont_touch = "true" *) INV u_inv2 (.out(clkout), .in(clknext));

endmodule
