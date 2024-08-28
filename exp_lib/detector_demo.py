from __future__ import annotations

from typing import Any, Tuple

from .detector_base import DetectorBase
from .registry import register_detector

import asyncio
import random

class DetectorDemo(DetectorBase):
    def __init__(self):
        pass

    @staticmethod
    async def factory(data) -> DetectorBase:
        return DetectorDemo()
    
    def serilaize_inner(self) -> dict:
        return {}

    def get_measure_desc(self) -> list[str]:
        return ["val"]

    def get_struct_format(self) -> str:
        return "f"
    
    def get_print_format(self) -> list[str]:
        return ["%f"]
    
    async def set_var(self, id: str, val: Any):
        print(f"Detector {id} set to {val}")
    
    async def measure(self) -> Tuple[Any, ...]:
        return (random.random(),)

    async def run(self):
        while True:
            await asyncio.sleep(1)

register_detector(DetectorDemo)