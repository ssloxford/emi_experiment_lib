from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Tuple

import asyncio

class DetectorBase(ABC):
    def __init__(self):
        pass

    @staticmethod
    @abstractmethod
    async def factory(data) -> DetectorBase:
        pass

    def serilaize(self) -> dict:
        return {"type": self.__class__.__name__} | self.serilaize_inner()

    @abstractmethod
    def serilaize_inner(self) -> dict:
        return {}

    @abstractmethod
    def get_measure_desc(self) -> list[str]:
        return ["val"]

    @abstractmethod
    def get_struct_format(self) -> str:
        return "I"
    
    @abstractmethod    
    def get_print_format(self) -> list[str]:
        return ["%i"]
    
    @abstractmethod
    async def measure(self) -> Tuple[Any, ...]:
        return (0,)

    async def set_var(self, id: str, val: Any):
        pass

    @abstractmethod
    async def run(self):
        while True:
            await asyncio.sleep(1)