from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterator, Iterable
from typing import Any, Tuple
from .utils import VariableData

import os
import asyncio
import time

import json

from .generator_base import GeneratorBase
from .detector_base import DetectorBase

class ExperimentBase:
    current_var: Iterable[Any]

    def __init__(self, delay_s: float, generator: GeneratorBase | None, detector: DetectorBase | None, variables: list[VariableData]):
        self.delay_s = delay_s
        self.generator = generator
        self.detector = detector

        self.variables = variables
        self.has_on_variable = False
        for var in self.variables:
            if var.id == "on":
                self.has_on_variable = True

    @abstractmethod
    def get_next_vars(self) -> Iterable[Any]:
        pass

    async def _set_var(self, id: str, val: Any) -> None:
            if self.generator is not None:
                self.generator.set_var(id, val)
            if self.detector is not None:
                await self.detector.set_var(id, val)

    async def _set_next(self) -> bool:
        try:
            self.current_var = self.get_next_vars()

            for meta, val in zip(self.variables, self.current_var):
                # As of now, variables are strictly set in the order given by self.variables
                # Pooling all awaits is not allowed
                await self._set_var(meta.id, val)
        except StopIteration:
            return True
        return False

    async def on_value(self, measurement: Tuple[Any, ...]) -> bool:
        return True

    async def run(self):
        detector_task = None
        try:
            #Start generator
            if self.generator is not None:
                print("Starting generator")
                self.generator.start()

            # Start detector and detector task
            if self.detector is not None:
                print("Starting detector")
                detector_task = asyncio.create_task(self.detector.run())

            if await self._set_next():
                raise StopAsyncIteration()

            #If "on" isn't user controlled, set it automatically
            if not self.has_on_variable:
                await self._set_var("on", True)

            print("Starting measurements in 2 seconds")
            await asyncio.sleep(2)

            print("Starting measurements")
            while (detector_task is None) or (not detector_task.done()):
                #Wait for measurements
                await asyncio.sleep(self.delay_s)

                #Read measurements
                if self.detector is not None:
                    # Detector can raise StopAsyncIteration()
                    res = await self.detector.measure()
                else:
                    res = ()

                if await self.on_value(res):
                    break
                if await self._set_next():
                    break
        
        except StopAsyncIteration:
            print("End of iteration, stopping")
        except asyncio.exceptions.CancelledError:
            print("Interrupted, stopping")
        
        #Turn off generator and detector
        if not self.has_on_variable:
            await self._set_var("on", False)
            
        #Stop detector task
        if detector_task is not None:
            print("Stopping detector")
            detector_task.cancel()
            try:
                await detector_task
            except asyncio.exceptions.CancelledError:
                pass
        #Stop generator
        if self.generator is not None:
            print("Stopping generator")
            self.generator.stop()
            self.generator.wait()
        
class ExperimentIterator(ExperimentBase):
    iter_cnt: int
    def __init__(self, delay_s: float, generator: GeneratorBase | None, detector: DetectorBase | None, variables: list[VariableData], data: Iterable[Iterable[Any]], resume: int = 0, **kwargs):
        super().__init__(delay_s, generator, detector, variables, **kwargs)
        self.iter_cnt = -1
        # Create iterator form iterable
        self.data = iter(data)
        for _ in range(resume):
            self.get_next_vars()

    def get_next_vars(self) -> Iterable[Any]:
        self.iter_cnt += 1
        return next(self.data)
    

class ExperimentLogger(ExperimentIterator):
    def __init__(self, delay_s: float, generator: GeneratorBase | None, detector: DetectorBase, savefile: str, user_metadata: dict, **kwargs):
        super().__init__(delay_s, generator, detector, **kwargs)

        #Find appropriate filename for data
        idx = 0
        while True:
            filename = f"{savefile}.{idx}.csv"
            if(not os.path.isfile(filename)):
                break
            idx += 1
        
        filename = os.path.abspath(filename)

        #Create parent folders
        os.makedirs(os.path.dirname(filename), exist_ok=True)

        #Only the name of the file
        filenameonly = os.path.basename(filename)

        #Open data file
        self.file = open(filename, "a")
        system_vars = [meta.print_format for meta in self.variables]
        detector_results = self.detector.get_print_format() if self.detector is not None else []
        format_entries = ["%s", "%i"] + system_vars + detector_results
        self.format = "\t".join(format_entries)

        #Assemble metadata
        main_metadata = {
            #Core metadata
            "v": "0.2.0",
            "time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "description": user_metadata.get("description"),
            #Data
            "columns": ["time", "it"] + [meta.id for meta in self.variables] + (self.detector.get_measure_desc() if self.detector is not None else []),
            "fmt_string": format_entries,
            "datafile": filenameonly,
            #Reproducability and detailed experiment info
            
        }
        user_metadata.pop("description", None)
        #Add user data
        main_metadata |= {
            "userdata": user_metadata
        }

        #Write metadata to file
        metafile = open(f"{savefile}.meta", "a")
        json.dump(main_metadata, metafile)
        metafile.write(",\n")
        metafile.close()


    async def on_value(self, measurements: Tuple[Any, ...]):
        line = (self.format + "\n") % (
            time.strftime("%Y-%m-%d %H:%M:%S"),
            self.iter_cnt,
            *self.current_var,
            *measurements
        )
        print(line, end="")
        self.file.write(line)
        self.file.flush()