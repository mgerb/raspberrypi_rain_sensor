# Raspberry Pi Rain Sensor

- raspberry pi zero
- python
- flask web framework
- sqlite

This is a small script to record and display rain data in the web browser.
Data is meant to be collected from a switch attached to GPIO pins. Each
reading represents 1/100 inches of rain. Data is grouped by the day
and displays in a simple table.

## Requirements

- python 3
- pip 3
- flask
- gpiozero

`pip3 install flask gpiozero`

Run with: `python3 main.py`

### How to run at startup

- clone this repo in the home directory
- copy `sensor_startup.sh` to the home directory
- `crontab -e`
- add the following line: `sh $HOME/sensor_startup.sh`
