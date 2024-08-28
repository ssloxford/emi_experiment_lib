from __future__ import annotations

from typing import Dict, Type

from .detector_base import DetectorBase
from .generator_base import GeneratorBase

detector_registry: Dict[str, Type[DetectorBase]] = {}
generator_registry: Dict[str, Type[GeneratorBase]] = {}


def register_detector(cl: Type[DetectorBase], name: str | None = None):
    if name is None:
        name = cl.__name__
    detector_registry[name] = cl

def register_generator(cl: Type[GeneratorBase], name: str | None = None):
    if name is None:
        name = cl.__name__
    generator_registry[name] = cl

def find_detector(name: str) -> Type[DetectorBase]:
    res = detector_registry.get(name)
    if res is None:
        raise KeyError
    return res

def find_generator(name: str) -> Type[GeneratorBase]:
    res = generator_registry.get(name)
    if res is None:
        raise KeyError
    return res