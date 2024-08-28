from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Tuple, Any

from .generator_base import GeneratorRFBase
from .rs_smc100a import RS_SMC100A
from .registry import register_generator
import math

class Generator_SMC100A(GeneratorRFBase):

    def __init__(self, visa_name: str | None = None):
        GeneratorRFBase.__init__(self)
        self.instr = RS_SMC100A(visa_name)
        self.instr.setRF(False)
        self.instr.setModOff()

    @staticmethod
    async def factory(data) -> Generator_SMC100A:
        return Generator_SMC100A(data["visa_name"])
    
    def serilaize_inner(self) -> dict:
        return {
            "visa_name": self.instr.name
        }

    def get_freq_range(self) -> Tuple[float,float]:
        return (8e3, 3.2e9)

    def set_freq(self):
        self.instr.setFrequency(self.freq)

    def get_power_range(self) -> Tuple[float,float]:
        return (-120.0, 19.0)

    def set_power(self):
        return self.instr.setPower(self.power)

    def start(self):
        pass

    def stop(self):
        self.instr.setRF(False)

    def set_var(self, id: str, val: Any):
        if id == "on":
            self.on = bool(val)
            if(self.on):
                #Make sure values were set before turning on
                assert(not math.isnan(self.freq))
                assert(not math.isnan(self.power))
            self.instr.setRF(self.on)
        else:
            super().set_var(id, val)

    def wait(self):
        pass
