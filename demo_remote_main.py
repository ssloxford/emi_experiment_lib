# Remote sensor module
# Accepts connections from a main system controlling the experiment, via a DetectorRemote()
# See demo_main.py for an example

from exp_lib.detector_demo import DetectorDemo
from exp_lib.remote_server import remote_main

import asyncio

if __name__ == '__main__':
    try:
        asyncio.run(remote_main(DetectorDemo()))
    except KeyboardInterrupt:
        print("Closing app")

# Does not close after running an experiment, it waits for the next one
# CTRL+C (SIGINT) to exit