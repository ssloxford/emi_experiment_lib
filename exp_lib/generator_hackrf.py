from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Tuple, Any

from .generator_sdr import GeneratorSDR

from gnuradio import soapy

from .registry import register_generator

class GeneratorHackRF(GeneratorSDR):
    amp_on: bool
    bandwidth: float

    def __init__(self, samp_rate: int, bandwidth = 6e6):
        self.amp_on = False
        self.bandwidth = bandwidth
        super().__init__(samp_rate)

    @staticmethod
    async def factory(data) -> GeneratorHackRF:
        return GeneratorHackRF(data["samp_rate"], data["bandwidth"])
    
    def serilaize_inner(self) -> dict:
        return {
            "samp_rate": self.samp_rate,
            "bandwidth": self.bandwidth
        }

    def init_sink(self):
        dev = 'driver=hackrf'
        stream_args = ''
        tune_args = ['']
        settings = ['']

        self.sink_0 = soapy.sink(dev, "fc32", 1, '', # type: ignore
                                stream_args, tune_args, settings)
        self.sink_0.set_sample_rate(0, self.samp_rate)
        self.sink_0.set_bandwidth(0, self.bandwidth)
        self.sink_0.set_frequency(0, self.get_freq_range()[0])
        self.sink_0.set_gain(0, 'AMP', False)
        self.sink_0.set_gain(0, 'VGA', self.get_power_range()[0])

    
    def get_freq_range(self) -> Tuple[float,float]:
        return (1e6, 6000e6)

    def set_freq(self):
        self.sink_0.set_frequency(0, self.freq)
        
    def get_power_range(self) -> Tuple[float,float]:
        return (0, 47.0)
    
    def set_power(self):
        self.sink_0.set_gain(0, 'VGA', self.power)
        
    def set_var(self, id: str, val: Any):
        if id == "amp":
            self.amp_on = bool(val)
            self.sink_0.set_gain(0, 'AMP', self.amp_on)
        else:
            super().set_var(id, val)
        
    def get_var(self, id: str):
        if id == "amp":
            return self.amp_on
        else:
            return super().get_var(id)