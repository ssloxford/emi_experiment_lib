from __future__ import annotations
from typing import NamedTuple, Mapping
import re
import serial
import serial.tools.list_ports

def find_serial(id: str|None, name_regex: str|None) -> str:
    while True:
        num_id = None
        # List ports
        ports = sorted(serial.tools.list_ports.comports())
        # Check if user supplied name is connected
        for pid, port in enumerate(ports):
            if port.device == id:
                num_id = pid
        if num_id is None:
            id = None
        
        # No name provided, or it can't be found
        # Ask user to select from all devices
        if num_id is None:
            input(f"Ensure device is connected")
            # Reload selection
            ports = sorted(serial.tools.list_ports.comports())
            print(f"Please select device")
            for idx, (port, desc, hwid) in enumerate(ports):
                print("{} \t {} {} [{}]".format(idx, port, desc, hwid))
            num_id = int(input("Number of option: "))

        # Get Identity string, for type checking of the device
        iden = ports[num_id].description
        # If user supplied test regex, check that instrument ID is as expected
        if(name_regex is not None):
            if re.match(name_regex, iden) is not None:
                print(f"Identity test match: {iden}")
                return ports[num_id].device
            else:
                print(f"Identity test failed: {iden} against {name_regex}")
                if(input("Accept? [y/n]") == "y"):
                    return ports[num_id].device
                id = None
                num_id = None
        else:
            print(f"Identity test: {iden}")
            if(input("Accept? [y/n]") == "y"):
                return ports[num_id].device
            id = None
            num_id = None