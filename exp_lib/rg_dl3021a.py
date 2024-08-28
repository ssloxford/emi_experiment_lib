from __future__ import annotations
from typing import Literal

from .visa_common import VisaDevice

class RG_DL3021A(VisaDevice):
    def __init__(self, name: str|None = None):
        super().__init__(name, "RIGOL TECHNOLOGIES,DL3021A")

    def getV(self):
        return float(self.query("MEAS:VOLT:DC?"))
    
    def getI(self):
        return float(self.query("MEAS:CURR:DC?"))
    
    def setLoadOn(self, on):
        on_str = "ON" if on else "OFF"
        self.send(f"SOUR:INP:STAT {on_str}")
    
    def setLoadMode(self, mode: Literal["VOLT","CURR","RES","POW"], value: float):
        self.send(f"SOUR:FUNC {mode}")
        self.send(f"SOUR:{mode}:LEV:IMM {value}")
        