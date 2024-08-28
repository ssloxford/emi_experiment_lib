from __future__ import annotations


from dataclasses import dataclass
from typing import Dict, Any, NamedTuple
import numpy as np
import json
import csv
import os

class DatasetRun(NamedTuple):
    time: str | None
    description: str | None
    
    data: Dict[str, np.ndarray]

    userdata: Any

    def filter(self, filter_bools):
        return DatasetRun(
            time = self.time,
            description= self.description,

            data = {k: v[filter_bools] for k, v in self.data.items()},

            userdata=self.userdata
        )
        

    @staticmethod
    def scanf(fmt: list[str], str: str):
        def parse_token(f, token):
            if f=="%i":
                return int(token)
            if f=="%f":
                return float(token)
            if f=="%s":
                return token

        tokens = str.split("\t")
        #print(len(tokens), len(fmt))
        assert(len(tokens) == len(fmt))
        return [parse_token(f, token) for f, token in zip(fmt, tokens)]

    @staticmethod
    def load_data_file(filename, columns, fmt):
        #Make columns unique
        col_counts = {}
        for key in columns:
            tmp = col_counts.get(key, (0,1))
            if tmp[0] == 1:
                print("Warning, duplicate keys {key} will be renamed")
            col_counts[key] = (1 + tmp[0],tmp[1])
        new_columns = []
        for key in columns:
            if col_counts[key][0] > 1:
                new_columns.append(f"{key}_{col_counts[key][1]}")
                
            else:
                new_columns.append(key)
            tmp = col_counts.get(key, (0,0))
            col_counts[key] = (tmp[0], tmp[1] + 1)

        data_lists = [[] for col in new_columns]
        with open(filename, newline='') as datafile:
            for row in datafile.readlines():
                entries = DatasetRun.scanf(fmt, row)
                assert(len(entries) == len(new_columns))
                for idx, entry in enumerate(entries):
                    data_lists[idx].append(entry)
        return {k: np.array(v) for k, v in zip(new_columns, data_lists)}

class Dataset(NamedTuple):
    runs: list[DatasetRun]

    def merge(self, run_data: list[Dict[str, Any]] | None = None):
        #Check that columns can be merged
        for run in self.runs:
            assert(run.data.keys() == self.runs[0].data.keys())

        if run_data is None:
            run_data = [{} for r in self.runs]
        #Check additional data
        for rd in run_data:
            assert(rd.keys() == run_data[0].keys())
        
        combined_data = {key: [] for key in (list(run_data[0].keys()) + list(self.runs[0].data.keys()))}
        for extra, run in zip(run_data, self.runs):
            run_lenght = len(run.data[list(run.data.keys())[0]])
            for key, value in extra.items():
                combined_data[key].append(np.array([value for i in range(run_lenght)]))
            for key, value in run.data.items():
                combined_data[key].append(value)
        flat_data = {}
        for key, value in combined_data.items():
            flat_data[key] = np.concatenate(value)
        return DatasetRun(
            time = None,
            description = None,
            data = flat_data,
            userdata = None)

def load_dataset(meta_file):
    file = open(meta_file + ".meta", "r")
    file_content = file.read().strip("\r\n\t ,")
    json_str = f"[{file_content}]"
    metadata = json.loads(json_str)
    runs = []
    for entry in metadata:
        if entry["v"] == "0.2.0":
            runs.append(DatasetRun(
                time = entry["time"],
                description = entry["description"],

                data = DatasetRun.load_data_file(os.path.join(os.path.dirname(meta_file), entry["datafile"]), entry["columns"], entry["fmt_string"]),

                userdata = entry["userdata"])
            )
    return Dataset(runs)
