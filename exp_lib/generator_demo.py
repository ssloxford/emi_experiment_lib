from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Tuple, Any

from .generator_base import GeneratorBase

from .registry import register_generator

class GeneratorDemo(GeneratorBase):
    freq: float
    power: float

    def __init__(self):
        self.freq = 0
        self.power = 0

    @staticmethod
    async def factory(data) -> GeneratorBase:
        return GeneratorDemo()
    
    def serilaize_inner(self) -> dict:
        return {}

    def get_var_range(self, id: str) -> Tuple[float,float] | Tuple[None, None]:
        if id == "freq":
            return (0, 10e9)
        elif id == "power":
            return (-100, 50)
        else:
            return (None, None)
        
    def get_var(self, id: str) -> float | None:
        if id == "freq":
            return self.freq
        elif id == "power":
            return self.power
        else:
            return None
        
    def set_var(self, id: str, val: Any):
        if id == "freq":
            self.freq = val
        elif id == "power":
            self.power = val
            
        print(f"Generator {id} set to {val}")

    def start(self):
        pass
    def stop(self):
        pass
    def wait(self):
        pass
