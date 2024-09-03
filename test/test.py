# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer

@cocotb.test()
async def test_shift_register(dut):
    """Test the parameterized shift register with internal two-phase clock generation."""
    
    # Create a 10ns period clock on dut.clk
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())

    # Reset the DUT
    dut._log.info("Resetting the shift register")
    dut.rst_n.value = 0
    await Timer(20, units="ns")  # Wait for 20 ns
    dut.rst_n.value = 1
    await RisingEdge(dut.clk)  # Wait for a clock cycle after reset

    # Initialize input
    dut.ui_in.value = 1  # Set the input to 1
    dut._log.info("Applying input: %d", dut.ui_in.value)

    # Shift the input through the register for SR_LEN + 1 cycles
    SR_LEN = int(dut.SR_LEN)
    for i in range(SR_LEN + 1):
        await RisingEdge(dut.clk)
        await Timer(10, units="ns")  # Allow time for clock phases to update
        dut._log.info(f"Cycle {i}: uo_out = {int(dut.uo_out.value)}")

    # Check if the output matches the expected shift behavior
    expected_output = 1  # Since we shifted in '1', we expect the last bit to be '1'
    assert dut.uo_out.value == expected_output, f"Test failed: expected {expected_output}, got {int(dut.uo_out.value)}"

    # Test shifting in zeroes
    dut.ui_in.value = 0  # Change input to 0
    dut._log.info("Applying input: %d", dut.ui_in.value)

    for i in range(SR_LEN):
        await RisingEdge(dut.clk)
        await Timer(10, units="ns")  # Allow time for clock phases to update
        dut._log.info(f"Cycle {SR_LEN + 1 + i}: uo_out = {int(dut.uo_out.value)}")

    # After shifting SR_LEN zeroes, the output should be zero
    assert dut.uo_out.value == 0, f"Test failed: expected 0, got {int(dut.uo_out.value)}"

    dut._log.info("Test completed successfully.")