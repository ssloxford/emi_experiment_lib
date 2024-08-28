import asyncio
import time
import socket
import struct

from .detector_base import DetectorBase
from .net_utils import *
from .utils import VariableData

async def remote_main(detector: DetectorBase, port: int = 41968):

    async def handle_connection(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        addr = writer.get_extra_info('peername')
        print(f"Connection from {addr!r}")

        async def send_res(data: bytes):
            writer.write(data)
            await writer.drain()

        while True:
            try:
                pkt_id = (await read_and_decode("I", reader))[0]

                # Login handshake
                if(pkt_id == 0x70):
                    data_content = (await read_and_decode("I", reader))[0]
                    if(data_content == 0x1337):
                        await send_res(struct.pack("I", 0x4201))
                    else:
                        await send_res(struct.pack("I", 0))

                # Struct format query
                if(pkt_id == 0x71):
                    await send_res(
                        pack_string(detector.get_struct_format()) + 
                        pack_string(str(detector.get_print_format())) +
                        pack_string(str(detector.get_measure_desc()))
                    )

                # Measure query
                if(pkt_id == 0x78):
                    measurement = await detector.measure()
                    await send_res(struct.pack(detector.get_struct_format(), *measurement))

                # Variable update
                if(pkt_id == 0x80):
                    id = await read_string(reader)
                    format, value = (await read_struct(reader))
                    await detector.set_var(id, value[0])
                if(pkt_id == 0x81):
                    id = await read_string(reader)
                    value = (await read_string(reader))
                    await detector.set_var(id, value)

            except asyncio.exceptions.IncompleteReadError:
                print("Connection closed")
                break


    server = await asyncio.start_server(
        handle_connection, '', port)

    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')

    async def run_detector():
        await detector.run()
        print("Closing server")
        server.close()

    main_loop = asyncio.ensure_future(run_detector())

    try:
        async with server:
            await server.serve_forever()
    except asyncio.exceptions.CancelledError:
        pass