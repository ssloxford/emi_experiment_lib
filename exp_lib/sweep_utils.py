from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Tuple
import itertools

import math
import numpy as np

def generate_freqs(freq_start: float, freq_step: float, freq_rel_step: float, freq_stop: float, banned_ranges: list[Tuple[float, float]] = []) -> list[float]:
    res = []

    freq = freq_start
    while freq <= freq_stop:
        res.append(freq)

        #Next step
        freq = freq * (1 + freq_rel_step) + freq_step

        #Skip banned ranges
        for banned_range in banned_ranges:
            if(banned_range[0] <= freq and freq < banned_range[1]):
                freq = banned_range[1]

    return res

def generate_powers_dBm(pow_start: float, pow_step: float, pow_stop: float) -> list[float]:
    res = []

    pow = pow_start
    while (pow <= pow_stop and pow_step > 0) or (pow >= pow_stop and pow_step < 0):
        res.append(pow)

        #Next step
        pow = pow + pow_step
    
    return res

def generate_powers_mW(pow_start: float, pow_step: float, pow_stop: float) -> list[float]:
    res = []

    pow = pow_start
    while (pow <= pow_stop and pow_step > 0) or (pow >= pow_stop and pow_step < 0):
        res.append(pow)

        #Next step
        pow = pow + pow_step
    
    #COnvert to dBm
    return list(10*np.log10(res))

def generate_all_combinations(*iterables, **kwargs):
    """Similar to itertools.product, but allow user to specify order of iteration.
    Use order=[...] to specify order in which inputs are scanned (highest number first).
    Equal priority means they are zipped
    """
    order = kwargs.get("order", list(range(len(iterables))))
    max_priority = max(*order)
    vals = [list(it) for it in iterables]
    def iterate_priority(n):
        parent_src = [[None for x in order]] if n == 0 else iterate_priority(n - 1)
        idxs = [idx for idx, val in enumerate(order) if val == n]
        for res in parent_src:    
            for i in range(len(vals[idxs[0]])):
                for idx in idxs:
                    res[idx] = vals[idx][i]
                yield res

    for x in iterate_priority(max_priority):
        yield tuple(x)

def generate_sequence(*iterables):
    return itertools.chain(*iterables)