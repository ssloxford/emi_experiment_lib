from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Tuple, Any

from .generator_base import GeneratorRFBase

import sys

from gnuradio import gr
from gnuradio import analog
import sys
import signal
import math

class GeneratorSDR(GeneratorRFBase, gr.top_block, ABC):
    samp_rate: int

    def __init__(self, samp_rate: int):
        self.samp_rate = samp_rate
        gr.top_block.__init__(self, "Signal generator", catch_exceptions=True)
        GeneratorRFBase.__init__(self)

        def shutdown(sig=None, frame=None):
            nonlocal self

            self.stop()
            self.wait()

            sys.exit(0)

        signal.signal(signal.SIGINT, shutdown)
        signal.signal(signal.SIGTERM, shutdown)
        
        self.init_sink()
        self.init_blocks()

    @abstractmethod
    def init_sink(self):
        # This function should set self.sink_0
        # Unless you are running a fancy configuration, and know what you are doing
        pass

    def init_blocks(self):
        #Default source is off, send constant 0s
        self.analog_const_source_x_0 = analog.sig_source_c(0, analog.GR_CONST_WAVE, 0, 0, 0)# type: ignore

        self.connect((self.analog_const_source_x_0, 0), (self.sink_0, 0))# type: ignore

    def get_var(self, id: str) -> Any:
        if id == "on":
            return self.on
        else:
            return super().get_var(id)
        
    def set_var(self, id: str, val: Any):
        if id == "on":
            self.on = bool(val)
            if(self.on):
                #Make sure values were set before turning on
                assert(not math.isnan(self.freq))
                assert(not math.isnan(self.power))
                self.analog_const_source_x_0.set_offset(1)
            else:
                self.analog_const_source_x_0.set_offset(0)
        else:
            super().set_var(id, val)

    def start(self):
        gr.top_block.start(self)
    def stop(self):
        gr.top_block.stop(self)
    def wait(self):
        gr.top_block.wait(self)