from __future__ import annotations
from typing import Literal

from .visa_common import VisaDevice

class RG_DS2302A(VisaDevice):
    def __init__(self, name: str|None = None):
        super().__init__(name, "RIGOL TECHNOLOGIES,DS2302A")

    def getVAvg(self, chan: int = 1):
        return float(self.query(f'MEAS:VAVG? CHAN{chan}'))

    def setBW(self, chan: int, value: Literal["20M","100M","OFF"]):
        self.send(f'CHAN{chan}:BWL {value}')

    def setCoupling(self, chan: int, value: Literal["AC","DC","GND"]):
        self.send(f'CHAN{chan}:COUP {value}')

    def setDisplay(self, chan: int, value: bool):
        self.send(f'CHAN{chan}:DISP {1 if value else 0}')
    
    def setInvert(self, chan: int, value: bool):
        self.send(f'CHAN{chan}:INV {1 if value else 0}')
    
    def setImpedance(self, chan: int, value: Literal["50","HI"]):
        self.send(f'CHAN{chan}:IMP {"FIFT" if value=="50" else "OMEG"}')
    
    def setOffset(self, chan: int, value: float):
        self.send(f'CHAN{chan}:OFFS {value}')

    def setScale(self, chan: int, value: float):
        self.send(f'CHAN{chan}:SCAL {value}')
    
    def setProbe(self, chan: int, value: float):
        self.send(f'CHAN{chan}:PROB {value}')
    
    def setTimebase(self, value: float):
        self.send(f'TIM:SCAL {value}')

    def setDefaults(self, chan: int):
        self.setBW(chan, "OFF")
        self.setCoupling(chan, "DC")
        self.setDisplay(chan, True)
        self.setInvert(chan, False)
        self.setImpedance(chan, "HI")
        self.setOffset(chan, 0)
        self.setScale(chan, 1)
        self.setProbe(chan, 1)
