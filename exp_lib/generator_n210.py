from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Tuple, NamedTuple

from .generator_sdr import GeneratorSDR
from .registry import register_generator

from gnuradio import uhd

class Daughterboard(NamedTuple):
    freq: Tuple[float, float]
    gain: Tuple[float, float]
    antenna: str

N210_daughter_boards = {
    "WBX": Daughterboard((68.75e6, 2200e6), (0, 31), "TX/RX")
}

class GeneratorN210(GeneratorSDR):
    def __init__(self, samp_rate: int, daughter_board = "WBX", ip: str|None=None):
        self.daughter_board = daughter_board
        self.board = N210_daughter_boards[daughter_board]
        self.ip = ip
        super().__init__(samp_rate)

    @staticmethod
    async def factory(data) -> GeneratorN210:
        return GeneratorN210(data["samp_rate"], data["daughter_board"])
    
    def serilaize_inner(self) -> dict:
        return {
            "samp_rate": self.samp_rate,
            "daughter_board": self.daughter_board
        }

    def init_sink(self):
        self.sink_0 = uhd.usrp_sink(# type: ignore
            ",".join((f"addr={self.ip}" if self.ip is not None else "", '')),
            uhd.stream_args(# type: ignore
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
            "",
        )
        self.sink_0.set_samp_rate(self.samp_rate)
        self.sink_0.set_center_freq(self.get_freq_range()[0], 0)
        self.sink_0.set_antenna(self.board.antenna, 0)
        self.sink_0.set_gain(self.get_power_range()[0], 0)

    def get_freq_range(self) -> Tuple[float,float]:
        return self.board.freq

    def set_freq(self):
        self.sink_0.set_center_freq(self.freq, 0)

    def get_power_range(self) -> Tuple[float,float]:
        return self.board.gain

    def set_power(self):
        self.sink_0.set_gain(self.power, 0)
