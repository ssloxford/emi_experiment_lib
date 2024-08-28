from __future__ import annotations

import asyncio
import struct
import ast
from typing import Any, Tuple

from .detector_base import DetectorBase
from .registry import register_detector
from .net_utils import *

class DetectorRemote(DetectorBase):
    struct_format: str
    print_format: str
    measure_desc: list[str]

    def __init__(self, address, port: int = 41968):
        self.address = address
        self.port = port
        pass

    @staticmethod
    async def factory(data) -> DetectorBase:
        res = DetectorRemote(data["address"], data["port"])
        await res.init()
        return res
    
    def serilaize_inner(self) -> dict:
        return {
            "attenuator": self.address,
            "port": self.port
        }

    async def init(self):
        self.reader, self.writer = await asyncio.open_connection(
            self.address, self.port)
        
        #Login
        await self._send(0x70, struct.pack("I", 0x1337))
        assert((await read_and_decode("I", self.reader))[0] == 0x4201)

        #Get struct and print format
        await self._send(0x71, b'')
        self.struct_format = await read_string(self.reader)
        self.print_format = ast.literal_eval(await read_string(self.reader))
        self.measure_desc = ast.literal_eval(await read_string(self.reader))

        return self

    async def _send(self, pkt: int, content: bytes):
        message = struct.pack("I", pkt) + content
        self.writer.write(message)
        await self.writer.drain()

    def get_measure_desc(self) -> list[str]:
        return self.measure_desc

    def get_struct_format(self):
        return self.struct_format
    
    def get_print_format(self):
        return self.print_format

    async def set_var(self, id: str, val: Any):
        if isinstance(val, int):
            await self._send(0x80, pack_string(id) + pack_struct("i", val))
        elif isinstance(val, float):
            await self._send(0x80, pack_string(id) + pack_struct("d", val))
        elif isinstance(val, str):
            await self._send(0x81, pack_string(id) + pack_string(val))
        else:
            assert(False)
        

    async def measure(self) -> Tuple[Any, ...]:
        try:
            await self._send(0x78, b'')
            return await read_and_decode(self.struct_format, self.reader)
        except asyncio.exceptions.IncompleteReadError:
            print("Connection closed")
            raise StopAsyncIteration

    async def run(self):
        try:
            while True:
                await asyncio.sleep(1)
        except asyncio.exceptions.CancelledError:
            self.writer.close()
            
register_detector(DetectorRemote)