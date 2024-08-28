from exp_lib.experiment_base import ExperimentLogger
from exp_lib.generator_demo import GeneratorDemo
from exp_lib.detector_demo import DetectorDemo
from exp_lib.detector_remote import DetectorRemote
from exp_lib.sweep_utils import generate_freqs, generate_powers_dBm, generate_all_combinations, generate_sequence
from exp_lib.utils import VariableData, format_freq

import asyncio

async def main():
    experiment = ExperimentLogger(
        0.5, #Delay between measurements

        GeneratorDemo(),

        #await DetectorRemote("127.0.0.1").init(), #Connect to sensor via the internet (make sure to start demo_remote_main.py)
        DetectorDemo(),

        #Variables being sweeped
        variables=[
            VariableData("freq", "%f", "Frequency", format_freq),
            VariableData("power", "%f", "Power"),
        ],

        # Values being sweeped through. Any finite Iterable[Tuple] is supported
        # Functons are built in for generating linear and logarithmic sweep patterns
        data=generate_sequence([(50e6, -100)], generate_all_combinations(
            generate_freqs(50e6, 0, 3, 1e9),
            generate_powers_dBm(0, -5, -7),
            order=[1,0]
        )),

        # Do not include filename
        # Metadata is automatically added to .meta
        # Data is saved in .###.csv files
        savefile="demo_data/test_exp",

        user_metadata={
            "description": "A first experiment",

            "location": "Your lab",
        },

        #Do not start at first. Can be used to resume experiment that had to be stopped.
        resume=3
    )
    await experiment.run()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Closing app")
