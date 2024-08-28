from abc import ABC, abstractmethod
from typing import Tuple, Any, Dict

from .generator_base import GeneratorBase
from .registry import register_generator, find_generator

class GeneratorMultiplex(GeneratorBase):
    generators: list[GeneratorBase]

    def __init__(self, generators):
        self.generators = generators

    @staticmethod
    async def factory(data) -> GeneratorBase:
        return GeneratorMultiplex([await find_generator(entry["type"]).factory(entry) for entry in data["nodes"]])
    
    def serilaize_inner(self) -> dict:
        return {
            "nodes": [det.serilaize() for det in self.generators]
        }
    
    def get_var_range(self, id: str) -> Tuple[Any,Any]:
        ress = [None, None]

        for gen in self.generators:
            res = gen.get_var_range(id)
            if res[0] is not None:
                if ress[0] is None or ress[0] < res[0]:
                    ress[0] = res[0]
            if res[1] is not None:
                if ress[1] is None or res[1] < ress[1]:
                    ress[1] = res[1]
        return (ress[0], ress[1])
        

    def get_var(self, id: str) -> Any:
        for gen in self.generators:
            res = gen.get_var(id)
            if res is not None:
                return res
        return None
    def set_var(self, id: str, val: Any):
        for gen in self.generators:
            gen.set_var(id, val)

    # Start the generator
    def start(self):
        for gen in self.generators:
            gen.start()
    # Stop the generator
    def stop(self):
        for gen in self.generators:
            gen.stop()
    # Wait for the generatopr to stop
    def wait(self):
        for gen in self.generators:
            gen.wait()

class GeneratorRename(GeneratorBase):
    rename: Dict[str, str]
    gen: GeneratorBase

    def __init__(self, gen, rename):
        self.gen = gen
        self.rename = rename

    def _getname(self, id: str):
        if id in self.rename:
            return self.rename[id]
        return id
    
    @staticmethod
    async def factory(data) -> GeneratorBase:
        return GeneratorRename(await find_generator(data["gen"]["type"]).factory(data["gen"]), data["rename"])
    
    def serilaize_inner(self) -> dict:
        return {
            "gen": self.gen.serilaize(),
            "rename": self.rename
        }

    def get_var_range(self, id: str) -> Tuple[Any,Any]:
        return self.gen.get_var_range(self._getname(id))
    def get_var(self, id: str) -> Any:
        return self.gen.get_var(self._getname(id))
    def set_var(self, id: str, val: Any):
        return self.gen.set_var(self._getname(id), val)

    # Start the generator
    def start(self):
        self.gen.start()
    # Stop the generator
    def stop(self):
        self.gen.stop()
    # Wait for the generatopr to stop
    def wait(self):
        self.gen.wait()
