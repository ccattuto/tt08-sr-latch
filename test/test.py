# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, FallingEdge, Timer

@cocotb.test()
async def test_shift_register(dut):
    """Test the shift register."""

    # Reset
    dut._log.info("Reset")
    dut.rst_n.value = 0
    await Timer(20, units="ns")  # Wait for 20 ns
    dut.rst_n.value = 1
    await Timer(20, units="ns")  # Wait for 20 ns

    dut.ui_in[2].value = 0

    # ---------------------------

    dut.ui_in[1].value = 0
    await Timer(10, units="ns")

    # fill shift register with 0s
    dut.ui_in[0].value = 0  # Set the input to 0
    await Timer(10, units="ns")
    dut._log.info("Applying input: %d", dut.ui_in[0].value)

    # Shift the input through the register for SR_LEN + 1 cycles
    SR_LEN = 512-64
    for i in range(SR_LEN):
        await Timer(10, units="ns")

        # toggle shift signal
        dut.ui_in[1].value = 1 - dut.ui_in[1].value
        await Timer(10, units="ns")

    dut._log.info(f"Cycle {i}: uo_out[0] = {int(dut.uo_out[0].value)}")

    # Check if the output matches the expected shift behavior
    assert dut.uo_out[0].value == 0, f"Test failed: expected 0, got {int(dut.uo_out[0].value)}"

    # ---------------------------

    dut.ui_in[1].value = 0
    await Timer(10, units="ns")

    # Test shifting in ones
    dut.ui_in[0].value = 1  # Change input to 1
    await Timer(10, units="ns")
    dut._log.info("Applying input: %d", dut.ui_in[0].value)

    SEQ_LEN = 17
    sum = 0
    for i in range(SR_LEN + SEQ_LEN * 2):
        await Timer(10, units="ns")

        # toggle shift signal
        dut.ui_in[1].value = 1 - dut.ui_in[1].value
        await Timer(10, units="ns")

        dut._log.info(f"Cycle {i}: uo_out[0] = {int(dut.uo_out[0].value)}")

        if i == SEQ_LEN - 1:
            dut.ui_in[0].value = 0

        sum = sum + int(dut.uo_out[0].value)

    # After shifting SR_LEN ones, the output should be one
    assert dut.uo_out[0].value == 0, f"Test failed: expected 1, got {int(dut.uo_out[0].value)}"

    assert sum == SEQ_LEN, f"Test failed: expected {SEQ_LEN}, got {sum}"

    dut._log.info("Test completed successfully.")
