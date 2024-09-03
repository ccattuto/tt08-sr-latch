<!---

This file is used to generate your project datasheet. Please fill in the information below and delete any unused
sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than
512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works

Shift register implemented by using D latches - rather than D flip flops - and a two-phase control clock, where one phase clocks the even latches and the other clocks the odd latches.

## How to test

Shift zeros into the register until the shift register contains all zeros. Then shift in a single 1 value and observe it periodically appear on the output signal of the shift register.

## External hardware

No external hardware required.
