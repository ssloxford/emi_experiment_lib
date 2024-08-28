Python package for automated measurement sweeps.

This package is designed to facilitate automatic parametric sweep measurements, varying multiple generators (outputs), and measuring multiple sensors (detectors).

Any local sensor can also be connected over the internet (e.g. wifi connection), to ensure galvanic isolation.

## Supported modules

New modules can easily be added, and the following are currently supported:

- VISA data source: Intrumnents conforming to the NI VISA specification.
  - Rigol DS2302 oscilloscope: Set channel mode, and query trace average voltage.
  - Rigol DL3021 digial load: Set load mode, and query voltage/current
  - R&S SMC 100A: Generate signals with controllable frequency and amplitude
- SDR devices
  - USRP N210, HackRF: Generate signals with controllable frequency and output gain.
- Low cost serial power meter
- Arbitary serial data source: device periodically sending numbers over serial

To implement a new module, identify the most similair already existing one, and copy it.
Rename the class accordingly, and be sure to define all the mandatory functions of the base class.

## Data saving

Data is saved with added metadata: the sweeps are saved to simple csv files, and additional metadata files are created to describe the file headers.
Running multiple experiments with the same output file name is supported. New csv-s are created for each, and the entries are listed in a shared metadata file.

## Installation

In the root folder (folder containing this `readme.md`), run `pip install .`

After making changes run `pip install --upgrade .`

Tested under Python 3.9 on Windows.
Only standard packages are used, so other systems should also work.

## Examples

`demo_main.py` contains a simple demo experiment using only "demo" generators and detectors, thus needs no hardware to run.

`demo_remote_main.py` shows how to set up a remote sensor module. Swap the line in `demo_main.py` to connect to the remote instead of a local sensor.

`demo_loader.py` demonstrates loading a dataset, merging multiple different runs and filtering.

## VISA

VISA is a standard for controlling scientific instruments, supported by a variety of devices from most benchtop lab equipment manufacturers.
The standard defines a text based transport layer, and basic control messages, but it does not define standardized messages for specific tasks.
I.e. different oscilloscopes from different vendors will use different messages to set parameters and query measurements.

This library currently only implements the specific instruments used by the authors, however in many cases it should be easy to copy the relevant files and replace the VISA commands.

When connecting to a VISA device (e.g. `DetectorDS2302A`), the address can be provided to the constructor.
This can be an IP address, or a USB VISA address.
If `None` is provided, the library will list all connected VISA devices, allowing interactive command line selection.
It is recommended to copy the selected ID into the code for seamless operation on future experiments.
For further information about addresses, consult the `pyvisa` documentation.