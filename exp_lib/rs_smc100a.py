from __future__ import annotations

from .visa_common import VisaDevice

class RS_SMC100A(VisaDevice):
    def __init__(self, name: str|None = None):
        super().__init__(name, "Rohde&Schwarz,SMC100A")

        self.setModOff()
        self.setRF(False)

    def setFrequency(self, freq_Hz):
        self.send(f"SOUR1:FREQ {freq_Hz}")
    def getFrequency(self):
        return float(self.query("SOUR1:FREQ?"))

    def setPower(self, power_dBm):
        self.send(f"SOUR1:POW {power_dBm}")
    def getPower(self):
        return float(self.query("SOUR1:POW?"))

    def setRF(self, on):
        on_str = "ON" if on else "OFF"
        self.send(f"OUTP {on_str}")

    def setModOff(self):
        self.send("SOUR1:MOD:ALL:STAT OFF")
    