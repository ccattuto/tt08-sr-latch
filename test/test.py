# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer

@cocotb.test()
async def test_shift_register(dut):
    """Test the parameterized shift register with internal two-phase clock generation."""
    
    # Create a 50ns period clock on dut.clk (20 MHz)
    clock = Clock(dut.clk, 50, units="ns")
    cocotb.start_soon(clock.start())

    # Reset the DUT
    dut._log.info("Resetting the shift register")
    dut.rst_n.value = 0
    await Timer(20, units="ns")  # Wait for 20 ns
    dut.rst_n.value = 1
    await RisingEdge(dut.clk)  # Wait for a clock cycle after reset

    # Initialize input
    dut.ui_in[0].value = 0  # Set the input to 0
    await Timer(10, units="ns")
    dut._log.info("Applying input: %d", dut.ui_in[0].value)

    # Shift the input through the register for SR_LEN + 1 cycles
    SR_LEN = 128
    for i in range(2 * SR_LEN):
        await RisingEdge(dut.clk)
        await Timer(10, units="ns")  # Allow time for clock phases to update
        dut._log.info(f"Cycle {i}: uo_out[0] = {int(dut.uo_out[0].value)}")

    # Check if the output matches the expected shift behavior
    assert dut.uo_out[0].value == 0, f"Test failed: expected 0, got {int(dut.uo_out[0].value)}"

    # Test shifting in ones
    dut.ui_in[0].value = 1  # Change input to 1
    await Timer(10, units="ns")
    dut._log.info("Applying input: %d", dut.ui_in[0].value)

    for i in range(2 * SR_LEN):
        await RisingEdge(dut.clk)
        await Timer(10, units="ns")  # Allow time for clock phases to update
        dut._log.info(f"Cycle {i}: uo_out[0] = {int(dut.uo_out[0].value)}")

    # After shifting SR_LEN ones, the output should be one
    assert dut.uo_out[0].value == 1, f"Test failed: expected 1, got {int(dut.uo_out[0].value)}"

    dut._log.info("Test completed successfully.")
