from __future__ import annotations
import pyvisa as visa
import re

class VisaDevice:
    def __init__(self, name: str|None = None, id_regex: str|None = None):
        self.instrument: visa.resources.Resource | None
        self.name: str

        print(f"Looking for {self.__class__.__name__} with Visa ID {name}")

        rm = visa.ResourceManager()
        while True:
            # No name provided
            # Ask user to select from all devices (excluding TCPIP)
            if name is None:
                # List all devices
                input(f"Ensure device is connected")
                res = rm.list_resources()
                print(f"Please select device")
                for idx, r in enumerate(res):
                    print(f"{idx} \t {r}")
                chosen = int(input("Number of option: "))
                name = res[chosen]

            #Try opening instrument
            # Don't validate that it is on resource list, since TCPIP devices don't show up
            try:
                print(f"Opening {name}")
                self.instrument = rm.open_resource(name)
                self.name = name
                print(f"Connected to device {name}")
                
                # Get Identity string, for type checking of the device
                iden = self.query("*IDN?")
                # If user supplied test regex, check that instrument ID is as expected
                if(id_regex is not None):
                    if re.match(id_regex, iden) is not None:
                        print(f"Identity test match: {iden}")
                        break
                    else:
                        print(f"Identity test failed: {iden} against {id_regex}")
                        if(input("Accept? [y/n]") == "y"):
                            break
                        name = None
                else:
                    print(f"Identity test: {iden}")
                    if(input("Accept? [y/n]") == "y"):
                        break
                    name = None
            except Exception:
                self.instrument = None
                name = None
                print(f"Could not find device {name}")
            

    def query(self, message):
        return self.instrument.query(message)# type: ignore
    def send(self, message):
        return self.instrument.write(message)# type: ignore
    def wait(self):
        self.send("*WAI")