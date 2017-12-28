FROM resin/rpi-raspbian:jessie

RUN apt-get update && apt-get -y upgrade && \
    apt-get install -y \
    ca-certificates \
    build-essential \
    wget \
    libdbus-1-dev libdbus-glib-1-dev libglib2.0-dev libical-dev libreadline-dev libudev-dev libusb-dev glib2.0 bluetooth bluez libbluetooth-dev \
    git \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Install Nodejs
RUN wget http://node-arm.herokuapp.com/node_latest_armhf.deb && \
    dpkg -i node_latest_armhf.deb && \
    rm -f node_latest_armhf.deb

#RUN useradd -ms /bin/bash pi
#USER pi

# Download node-flower-bridge
RUN git clone -b v2 https://github.com/Parrot-Developers/node-flower-bridge.git /home/pi/node-flower-bridge/

WORKDIR /home/pi/node-flower-bridge
RUN ./install.sh

COPY entrypoint.sh /home/pi/node-flower-bridge/entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
#ENTRYPOINT ["./bridge"]
#CMD ["display"]
