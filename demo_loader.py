from exp_lib.data_manager import *

#run demo_main twice to generate necessary data

#Load dataset
set = load_dataset("demo_data/test_exp")
print(set.runs[0].data)

#Merge various runs, and optionally add additional columns to each file
merged = set.merge([{"r": 0}, {"r": 1}])
print(merged.data)

#Filter based on various columns
filtered = merged.filter(merged.data["freq"] == 50000000)
print(filtered.data)