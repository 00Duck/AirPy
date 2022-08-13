# Installation Instructions

This folder is its own Python program and can be separated from the ../sensor_info_collector folder.

Basic steps are as follows:
- Install MariaDB and Prerequisite Software
- Install and configure server
- Set up Gunicorn
- Create and configure a Service

# Install MariaDB and Prerequisite Software

Run the following:

`sudo apt update && sudo apt install git python3-venv mariadb-server mariadb-backup libmariadb-dev`

Run secure install, answering yes/no as needed.

`sudo mysql_secure_installation`

Connect to the database using `sudo mariadb` or `mariadb -u root -p`

Once in MariaDB, run the following commands:

```sql
CREATE DATABASE airpy DEFAULT CHARACTER SET utf8 COLLATE utf8_unicode_ci;
GRANT ALL ON airpy.* TO 'airpy'@'localhost' IDENTIFIED BY 'airpy';
FLUSH PRIVILEGES;
EXIT;
```

# Install and Configure Server

Set up a virtual environment and install required Python dependencies:

```sh
cd Airpy/server
python3 -m venv env
source env/bin/activate
python -m pip install -r requirements.txt
pip install gunicorn
deactivate
```

At this point you may test the server directly by running `python3 server.py`. Stop the server using `CTRL + C`.

The most basic form of Gunicorn can be run using the following command. Please note that it is normally recommended for Gunicorn to be set up behind an Nginx proxy; however, I have not done this as the server will only be hosted in a local, closed environment.

`gunicorn --bind 0.0.0.0:5000 wsgi:app`

You may test using this command to ensure the server starts correctly with Gunicorn. Also note the port in case you decide to change it later.

Create a Service in `/etc/systemd/system` called airpy.service with the following details. Note that the below gunicorn

```ini
[Unit]
Description=AirPy Server
After=network.target
StartLimitIntervalSec=0

[Service]
User=www-data
Type=simple
Restart=always
RestartSec=5
WorkingDirectory=/srv/AirPy/server
ExecStart=env/bin/gunicorn --bind 0.0.0.0:5000 wsgi:app

[Install]
WantedBy=multi-user.target

```

Save the file. Start it using the following:

`sudo systemctl start airpy.service`

To run the server on start, use:

`sudo systemctl enable airpy.service`