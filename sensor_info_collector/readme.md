Install prerequisite software:

`sudo apt update && sudo apt install git python3-venv`

Clone down the git repo:

`cd /srv && git clone https://github.com/00Duck/AirPy.git`

Set up a virtual environment and install required Python dependencies:

```sh
cd Airpy/sensor_info_collector
python3 -m venv env
source env/bin/activate
python -m pip install -r requirements.txt
deactivate
```

Edit the config.ini file and set credentials to the server that you have already or will soon configure.

Run a test:

`env/bin/python main.py`

Run crontab -e and install the following. This will tell the Pi to collect and send data to the server every 30th minute.

`*/30 * * * * cd /srv/AirPy/sensor_info_collector && env/bin/python main.py`