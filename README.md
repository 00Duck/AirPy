# AirPy

A data collector script for the SDS011 sensor.

## The Setup

The idea behind this project is to hook the SDS011 to a Raspberry Pi (or any small form machine) and have it run periodically to collect air quality data. This software can be found in the `sensor_info_collector` folder. Since the Pi runs on flash storage, a separate program in the `server` folder can be run on another machine to collect the data via REST endpoint. A crontab on the Pi will determine the frequency at which data is sent. Finally, the data is made available for your viewing pleasure using Plotly by visiting the `server` you set up for database data collection.

## Cool. Now what?

Check out the readme.md file in each folder for corresponding instructions on installing components.