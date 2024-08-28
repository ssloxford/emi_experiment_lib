from __future__ import annotations

import math
from typing import Tuple, NamedTuple, Any, Callable


def format_prefix(number: float) -> str:
    number = float(number)
    #-18 to 18
    prefixes = ["a", "f", "p", "n", "u", "m", "", "k", "M", "G", "T", "P", "E"]

    abs_num = abs(number)
    if(abs_num < 1e-18 or abs_num >= 1e21):
        if(abs_num == 0):
            return "0"
        else:
            return "{:.3e}".format(number)
    
    #Within SI range [1e-18, 1e21)
    log_f = math.log10(abs_num)
    prefix_class = int(log_f // 3)
    prefix_class = min(max(-6, prefix_class), 6)
    
    multiplier = 10 ** (-3 * prefix_class)
    classed_num = number * multiplier
    fmt_str = "{:." + str(int(3 - (math.floor(log_f) % 3))) + "f}"
    return fmt_str.format(classed_num) + prefixes[6 + prefix_class]

def format_freq(freq_hz: float) -> str:
    return format_prefix(freq_hz) + "Hz"


class VariableData(NamedTuple):
    #id for set_var tests
    id: str
    #format string eg %f
    print_format: str
    #display name
    name: str
    #for user printing
    print_fn: Callable[[Any],str] | None = None

    def user_format(self, val: Any):
        if self.print_fn is not None:
            return self.print_fn(val)
        if self.print_format is not None:
            return self.print_format.format(val)
        return str(val)

    def user_name(self):
        if self.name is None:
            return self.id
        return self.id
