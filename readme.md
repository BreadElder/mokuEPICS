# Overview
This repository contains code that connects the Liquid instruments Moku devices to EPICS using pyDevSup and the python API for the device.

# Status
Early work in Progress, need to add in more of the settings for each instruments I have started and add the rest of the range of Instruments

# Features
- Oscilliscope
    - data in as waveforms
- Spectrum Analyser
    - data in as waveforms
- Switching Between instruments

# TODOs
- Convert from a single IOC to support elements that can be included more easily
- More instrument settings
- More of the instruments

# Installing

1. Generate a blank IOC. Must include the pyDevSup elements
2. Include the mokuSup and mokuApp directories in the IOC
3. pip install moku, this must be done as the user that is running the IOC
4. install the bitstream elements for moku: moku download --fw_ver=<ver>