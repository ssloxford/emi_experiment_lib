from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Tuple

from .detector_base import DetectorBase
from .registry import register_detector, find_detector

import asyncio

# Combine multiple detectors into a single concatenated measurement list
class DetectorMultiplex(DetectorBase):
    def __init__(self, detectors: list[DetectorBase]):
        self.detectors = detectors

    @staticmethod
    async def factory(data) -> DetectorBase:
        return DetectorMultiplex([await find_detector(entry["type"]).factory(entry) for entry in data["nodes"]])
    
    def serilaize_inner(self) -> dict:
        return {
            "nodes": [det.serilaize() for det in self.detectors]
        }

    def get_measure_desc(self) -> list[str]:
        return [f for det in self.detectors for f in det.get_measure_desc()]

    def get_struct_format(self) -> str:
        return "".join([det.get_struct_format() for det in self.detectors])
    
    def get_print_format(self) -> list[str]:
        return [f for det in self.detectors for f in det.get_print_format()]
    
    async def measure(self) -> Tuple[Any, ...]:
        measurements = [await det.measure() for det in self.detectors]
        return tuple(val for meas in measurements for val in meas)

    async def set_var(self, id: str, val: Any):
        for det in self.detectors:
            await det.set_var(id, val)

    async def run(self):
        while True:
            await asyncio.sleep(1)

register_detector(DetectorMultiplex)