from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Tuple

from .generator_sdr import GeneratorSDR
from .registry import register_generator

from gnuradio import soapy

class GeneratorPluto(GeneratorSDR):

    def __init__(self, samp_rate: int):
        super().__init__(samp_rate)

    @staticmethod
    async def factory(data) -> GeneratorPluto:
        return GeneratorPluto(data["samp_rate"])
    
    def serilaize_inner(self) -> dict:
        return {
            "samp_rate": self.samp_rate
        }

    def init_sink(self):
        dev = 'driver=plutosdr'
        stream_args = ''
        tune_args = ['']
        settings = ['']

        self.sink_0 = soapy.sink(dev, "fc32", 1, '', # type: ignore
                                stream_args, tune_args, settings)
        self.sink_0.set_sample_rate(0, self.samp_rate)
        self.sink_0.set_bandwidth(0, 0.0)
        self.sink_0.set_frequency(0, self.get_freq_range()[0])
        self.sink_0.set_gain(self.get_power_range()[0])

    def get_freq_range(self) -> Tuple[float,float]:
        #Non-unlocked
        #return (325e6, 3800e6)

        #Assumes unlocked firmware
        return (70e6, 6000e6)

    def set_freq(self):
        self.sink_0.set_frequency(0, self.freq)
        
    def get_power_range(self) -> Tuple[float,float]:
        return (0, 89.0)

    def set_power(self):
        self.sink_0.set_gain(0, self.power)
    