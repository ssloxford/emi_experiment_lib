from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Tuple

from .detector_base import DetectorBase
from .registry import register_detector
from .serial_common import find_serial

import asyncio
import serial
import serial.tools.list_ports
import math

class DetectorSimpleSerial(DetectorBase):
    def __init__(self, port: str, id_test: str | None = None, count = 1, separator = " "):
        print(f"Looking for serial device on {port}")
        self.port = find_serial(port, id_test)
        self.id_test = id_test
        self.ser = serial.Serial(port, 9600)
        self.ser.write(b'')
        self.count = count
        self.separator = separator
        self.struct_format = "f" * count
        self.print_format = ["%f"] * count

    @staticmethod
    async def factory(data) -> DetectorBase:
        return DetectorSimpleSerial(data["port"], data["id_test"], data["count"], data["separator"])
    
    def serilaize_inner(self) -> dict:
        return {
            "port": self.port,
            "id_test": self.id_test,
            "count": self.count,
            "separator": self.separator,
        }
    
    def get_measure_desc(self) -> list[str]:
        return [f"serial_{i+1}" for i in range(self.count)]

    def get_struct_format(self) -> str:
        return self.struct_format
    
    def get_print_format(self) -> list[str]:
        return self.print_format

    #Inform detector of attack frequency (if needed)
    async def set_var(self, id: str, val: Any):
        pass

    async def measure(self) -> Tuple[Any, ...]:
        #Ignore all queued rows
        while self.ser.in_waiting > 0:
            res = self.ser.read_until("\n".encode("ascii"), 50)
        #Flush measurement that was just being taken
        res = self.ser.read_until("\n".encode("ascii"))
        #Get a new row
        res = self.ser.read_until("\n".encode("ascii")).decode("ascii")
        res.strip("\n\r")
        return tuple(float(s) if len(s) else math.nan for s in res.split(self.separator))

    async def run(self):
        while True:
            await asyncio.sleep(1)

register_detector(DetectorSimpleSerial)