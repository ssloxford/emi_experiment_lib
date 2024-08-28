from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Tuple

from .detector_base import DetectorBase
from .rg_ds2302 import RG_DS2302A
from .registry import register_detector

import asyncio

class DetectorDS2302A(DetectorBase):
    instr: RG_DS2302A

    def __init__(self, visa_name: str | None = None, channels = [1], chan_multipliers = None, chan_names = None):
        self.instr = RG_DS2302A(visa_name)
        self.channels = channels
        self.chan_multipliers = chan_multipliers if chan_multipliers is not None else [1 for _ in range(len(channels))]
        self.chan_names = chan_names if chan_names is not None else [f"voltage_ds2302_ch{i}" for i in channels]

    @staticmethod
    async def factory(data) -> DetectorBase:
        return DetectorDS2302A(data["visa_name"], data["channels"])
    
    def serilaize_inner(self) -> dict:
        return {
            "visa_name": self.instr.name,
            "channels": self.channels,
            "chan_multipliers": self.chan_multipliers,
            "chan_names": self.chan_names,
            }

    def get_measure_desc(self) -> list[str]:
        return self.chan_names

    def get_struct_format(self) -> str:
        return "d" * len(self.channels)
    
    def get_print_format(self) -> list[str]:
        return ["%f" for c in self.channels]
    
    async def measure(self) -> Tuple[Any, ...]:
        return tuple(self.instr.getVAvg(ch) * chmul for ch, chmul in zip(self.channels, self.chan_multipliers))

    async def run(self):
        while True:
            await asyncio.sleep(1)

register_detector(DetectorDS2302A)