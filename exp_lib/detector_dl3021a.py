from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Tuple

from .detector_base import DetectorBase
from .rg_dl3021a import RG_DL3021A
from .registry import register_detector

import asyncio

class DetectorDL3021A(DetectorBase):
    instr: RG_DL3021A

    def __init__(self, visa_name: str | None = None):
        self.instr = RG_DL3021A(visa_name)

    @staticmethod
    async def factory(data) -> DetectorBase:
        return DetectorDL3021A(data["visa_name"])
    
    def serilaize_inner(self) -> dict:
        return {"visa_name": self.instr.name}

    def get_measure_desc(self) -> list[str]:
        return ["voltage_dl3021", "current_dl3021"]
        
    def get_struct_format(self) -> str:
        return "dd"
    
    def get_print_format(self) -> list[str]:
        return ["%f", "%f"]
    
    async def measure(self) -> Tuple[Any, ...]:
        return (self.instr.getV(), self.instr.getI())

    async def set_var(self, id: str, val: Any):
        if id == "dl3021_cv":
            self.instr.setLoadMode("VOLT", val)
        if id == "dl3021_cc":
            self.instr.setLoadMode("CURR", val)
        if id == "dl3021_cr":
            self.instr.setLoadMode("RES", val)
        if id == "dl3021_cp":
            self.instr.setLoadMode("POW", val)

    async def run(self):
        while True:
            await asyncio.sleep(1)

register_detector(DetectorDL3021A)