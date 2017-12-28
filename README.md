# Aquaponic Greenhouse

The goal of this repository is to share what I've created to monitor and automate my aquaponic greenhouse.
I tried to use docker almost everywhere to easily replicate/automate the setup and let everyone use it in a simple way.

# The setup

I have a raspberry pi 3 in my greenhouse with few sensors connected through I2C on it.
It currently monitors :
  * pH
  * Fishtank temperature
  * Humidity
  * Greenhouse temperature

Using a bridge to [flower power](http://global.parrot.com/au/products/flower-power/) it also monitors the light, the soil moisture, and fertilizer.
It uses this project: [https://github.com/Parrot-Developers/node-flower-bridge](https://github.com/Parrot-Developers/node-flower-bridge).

On the server side, because we need to store metrics and display them, I use a small Z83-V as a server. It's hosting a [grafana](https://grafana.com/) and an [influxdb](https://www.influxdata.com/).

## How to install it
### Client (in the greenhouse)
#### The packages
First, you will need to install your raspberry pi. I won't explain here how to do it, it's up to you to choose the distribution you prefer.

The packages needed are :
  * python3
  * python3-dev
  * pigpio
  * git
  
I let you install `docker` by yourself as it depends of your distribution, but [it's easy to do](https://www.raspberrypi.org/blog/docker-comes-to-raspberry-pi/)

Ideally, be sure you have `pip3` to install the following packages:
  * docker-compose
  * i2cdev
  * pigpio

Then, clone the repository :
```
git clone https://github.com/Seraf/greenhouse
```

#### The structure of the client
I created few directories in the client directory to sort a bit the different components.

  * `checks` directory contains all the checks (written in python to access the GPIO) to get the sensors values.
  * `crons` directory contains script that will be called as crons by your cron scheduler. It is used for example to recalibrate your pH sensor according the temperature changes.
  * `docker` directory contains the docker image source I used to create the containers I'm currently using.
  * `flower-power` directory should contains the credentials file to use if you have flower power devices. Else, ignore this directory.
  * `telegraf` directory contains the configuration I use to send values to the metrics database.
  * `docker-compose.yml` is the docker-compose file to launch all the containers

#### The configuration
##### Telegraf
Telegraf is an agent that will trigger the checks, get the values and send them to the metrics database.

The `telegraf/telegraf.conf` configuration file will need some changes according your own setup.

The main thing to change is the line :
```
[[outputs.influxdb]]
  urls = ["http://192.168.1.21:8086"] # required
```
You should obviously use the ip address of your server configured previously.

```
[[inputs.exec]]
  ## Commands array
  commands = [
    "/checks/htu21df.py",
    "/checks/flower_power.py",
    "/checks/ezoph.py",
    "/checks/ezotemp.py"
  ]
```
There is also the checks section to modify according your own sensors/checks.

##### Docker-compose
The `docker-compose.yml` file is simple when you already understand the concepts of docker.

It will launch 2 services : `telegraf` (the agent responsible to transmit data), and `flower-power` which is a bridge to my flower power devices.

If you don't have flower power devices, I recommend to remove all the lines concerned as it's not necessary (and don't forget to remove the check in the telegraf configuration)

#### Create the crons
Here are the crons I'm currently using:

```
13,28,43,58 * * * * /usr/bin/python3 /home/pi/greenhouse/client/crons/ph_calibration.py
0 12,15,18 * * *  /usr/bin/curl -X POST "http://192.168.1.21:8086/write?db=grafana&precision=s" --data-binary 'events title="Nourriture",text="Dose niveau 3"'
0 9 * * *  /usr/bin/curl -X POST "http://192.168.1.21:8086/write?db=grafana&precision=s" --data-binary 'events title="Nourriture",text="Dose niveau 4"'
```

The first one is to calibrate the pH sensor each 15 minutes according to the temperature change.

Why I didn't use `*/15` ? Because it's doing a read on the I2C interface at the same time than telegraf. Then, one of them is failing. To avoid that, I'm changing the temperature between two checks.

The two other crons are used to create annotations in my metrics database to have an annotation each time my auto-feeder is giving some food to fishes. Then I'm able to track the changes of other parameters according to the quantity of food delivered.

#### Launch it !
To launch the client, once configured, it's pretty simple, just execute this command :
```
pi@serre:~/greenhouse/client $ docker-compose up -d
```
