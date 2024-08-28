from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Tuple, Any

import math
class GeneratorBase(ABC):
    on: bool

    def __init__(self):
        self.on = False

    @staticmethod
    @abstractmethod
    async def factory(data) -> GeneratorBase:
        pass

    def serilaize(self) -> dict:
        return {"type": self.__class__.__name__} | self.serilaize_inner()

    @abstractmethod
    def serilaize_inner(self) -> dict:
        return {}

    @abstractmethod
    def get_var_range(self, id: str) -> Tuple[Any,Any]:
        pass
    @abstractmethod
    def get_var(self, id: str) -> Any:
        pass
    @abstractmethod
    def set_var(self, id: str, val: Any):
        pass

    # Start the generator
    @abstractmethod
    def start(self):
        pass
    # Stop the generator
    @abstractmethod
    def stop(self):
        pass
    # Wait for the generatopr to stop
    @abstractmethod
    def wait(self):
        pass


class GeneratorRFBase(GeneratorBase):
    freq: float
    power: float

    def __init__(self):
        self.freq = math.nan
        self.power = math.nan

    @abstractmethod
    def get_freq_range(self) -> Tuple[float,float]:
        pass

    @abstractmethod
    def set_freq(self):
        pass
        
    @abstractmethod
    def get_power_range(self) -> Tuple[float,float]:
        pass

    @abstractmethod
    def set_power(self):
        pass

    def get_var_range(self, id: str) -> Tuple[float,float] | Tuple[None, None]:
        if id == "freq":
            return self.get_freq_range()
        elif id == "power":
            return self.get_power_range()
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
            range = self.get_freq_range()
            self.freq = min(max(range[0], val), range[1])
            self.set_freq()
        elif id == "power":
            range = self.get_power_range()
            self.power = min(max(range[0], val), range[1])
            self.set_power()
        