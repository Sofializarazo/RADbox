# RADbox
Github repository to host the Arduino, python and executables for the Real-time Air Data box (RADbox) project.

## Table of Contents
- [Source Code Installation](#source-code-installation)
- [Executable Installation](#executable-installation)
- [Use](#use)

### Source Code Installation
The source code (arduino and python) can be found in the "source_code" directory. To modify/run this code manually, the following dependencies are required:
- **Python**:
  - pyserial v3.5 or newer[pyserial](https://pyserial.readthedocs.io/en/latest/)
  - matplotlib v3.6.3 or newer[matplotlib](https://matplotlib.org/stable/index.html)
  - seaborn v0.12.1 or newer[seaborn](https://seaborn.pydata.org/)

- **Arduino**:
  - Sparkfun SCD4x Arduino Library v1.1.2 [Sparkfun SCD4x Arduino Library](https://github.com/sparkfun/SparkFun_SCD4x_Arduino_Library)
  - Sensirion I2C SGP41 library v1.0.0 [Sensirion I2C SGP41 library](https://github.com/Sensirion/arduino-i2c-sgp41)
  - DFRobot_DHT20 library v1.0.0 [DFRobot_DHT20 library](https://github.com/DFRobot/DFRobot_DHT20)
  - (for RADbox) U8glib library v1.19.1 [U8glib library](https://github.com/olikraus/u8glib)

Note that code was written in Python 3.11.9 and Arduino version 2.2.1.

Using the source code directly is possible so long as the user has a version of Python (3.11) and Arduino is installed. Prepare the relevant Arduino by uploading the relevant .ino file to the board, to do this, follow the instructions found in the "instructions" directory in the setup Instructions file. 
### Executable Installation
To use the application, simply navigate to the Instructions directory and open either RADBox_lite Startup Guide.pdf or RADBox Startup Guide.pdf, depending on the device you are using. The guide clearly explains how to operate the system and what steps to follow if you wish to modify the code.

### Use
The RADbox was designed to teach students in the K-12 system about air-quality. It is capable of monitoring changes in CO<sub>2</sub>, VOCs, NO<sub>x</sub>, temperature and %humidity. To use the device, simply plug it in, run the software, and collect the relevant data. For a thorough guide, please see the published paper.





