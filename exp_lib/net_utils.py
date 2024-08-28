from __future__ import annotations

import struct
from typing import Tuple, Any
from asyncio import StreamReader

def pack_chunk(data: bytes) -> bytes:
    return struct.pack("I", len(data)) + data

def pack_string(str: str) -> bytes:
    return pack_chunk(str.encode("utf-8"))

def pack_struct(format: str, *args) -> bytes:
    return pack_string(format) + struct.pack(format, *args)


async def read_and_decode(format: str, reader: StreamReader) -> Tuple[Any, ...]:
    return struct.unpack(format, await reader.readexactly(struct.calcsize(format)))


async def read_chunk(reader: StreamReader) -> bytes:
    chunk_len = (await read_and_decode("I", reader))[0]
    return (await reader.readexactly(chunk_len))

async def read_string(reader: StreamReader) -> str:
    return (await read_chunk(reader)).decode("utf-8")

async def read_struct(reader: StreamReader) -> Tuple[str, Tuple[Any, ...]]:
    format = await read_string(reader)
    return (format, await read_and_decode(format, reader))
