from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Tuple

from .detector_base import DetectorBase
from .utils import VariableData
from .serial_common import find_serial
from .registry import register_detector

import asyncio
import serial
import serial.tools.list_ports

# Module to interface with cheaply available 1MHz-8GHz RF power meters using the AD8318 detector, and an onboard microcontroller

class DetectorPowermeter(DetectorBase):
    def __init__(self, port: str, attenuator: float = 0):
        print(f"Looking for power meter on {port}")
        self.port = find_serial(port, "USB-SERIAL CH340")
        self.attenuator = attenuator
        self.ser = serial.Serial(self.port, 9600)
        self.ser.write(b'')

    @staticmethod
    async def factory(data) -> DetectorBase:
        return DetectorPowermeter(data["port"], data["attenuator"])
    
    def serilaize_inner(self) -> dict:
        return {
            "port": self.port,
            "attenuator": self.attenuator
        }

    def get_measure_desc(self) -> list[str]:
        return ["dbm_pwm", "vpp_pwm"]

    def get_struct_format(self) -> str:
        return "ff"
    
    def get_print_format(self) -> list[str]:
        return ["%f", "%f"]

    #Inform detector of attack frequency (if needed)
    async def set_var(self, id: str, val: Any):
        if id == "freq":
            freq: float = val
            out_msg = "$" + ('0000{:.0f}'.format(freq / 1e6))[-4:] + "+" + ('0000{:.1f}'.format(self.attenuator))[-4:]
            self.ser.write(out_msg.encode(encoding="ascii"))

    async def measure(self) -> Tuple[Any, ...]:
        #Ignore all queued rows
        while self.ser.in_waiting > 0:
            res = self.ser.read_until("Vpp$".encode("ascii"), 50)
        #Flush measurement that was just being taken
        res = self.ser.read_until("Vpp$".encode("ascii"))
        #Get a new value
        res = self.ser.read_until("Vpp$".encode("ascii")).decode("ascii")
        pow_dbm = float(res[-21:-16].replace(" ", ""))
        prefix_mul = -1
        if res[-5] == "n":
            prefix_mul = 1e-9
        if res[-5] == "u":
            prefix_mul = 1e-6
        if res[-5] == "m":
            prefix_mul = 1e-3
        if res[-5] == " ":
            prefix_mul = 1
        pow_vpp = float(res[-11:-7].replace(" ", "")) * prefix_mul
        return (pow_dbm, pow_vpp)

    async def run(self):
        while True:
            await asyncio.sleep(1)

register_detector(DetectorPowermeter)