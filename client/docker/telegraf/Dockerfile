FROM resin/rpi-raspbian:jessie

RUN apt-get update && apt-get -y upgrade && \
    apt-get install -y \
    ca-certificates \
    wget \
    build-essential \
    libglib2.0-dev libdbus-1-dev libical-dev libreadline-dev libudev-dev libbluetooth-dev \
    python3 \
    python3-dev \
    python3-pip \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*


ENV BLUEZ_VERSION 5.49
RUN wget http://www.kernel.org/pub/linux/bluetooth/bluez-${BLUEZ_VERSION}.tar.gz && \
    tar -zxvf bluez-${BLUEZ_VERSION}.tar.gz && \
    cd bluez-${BLUEZ_VERSION} && \
    ./configure --prefix=/usr --sysconfdir=/etc --localstatedir=/var --enable-tools --disable-test --disable-systemd --enable-deprecated && \
    make all && \
    make install && \
    cp attrib/gatttool /usr/bin/ && \
    cd .. && \
    rm -fr bluez-${BLUEZ_VERSION}*

# Install Rpi.GPIO
RUN pip3 install pigpio
RUN pip3 install requests
RUN pip3 install miflora
RUN pip3 install pybluez

ENV TELEGRAF_VERSION 1.6.1-1
RUN wget -q https://dl.influxdata.com/telegraf/releases/telegraf_${TELEGRAF_VERSION}_armhf.deb && \
    dpkg -i telegraf_${TELEGRAF_VERSION}_armhf.deb && \
    rm -f telegraf_${TELEGRAF_VERSION}_armhf.deb*

EXPOSE 8125/udp 8092/udp 8094

COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
CMD ["telegraf"]
