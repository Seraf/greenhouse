FROM resin/rpi-raspbian:jessie

RUN apt-get update && apt-get -y upgrade && \
    apt-get install -y \
    ca-certificates \
    wget \
    build-essential \
    python3 \
    python3-dev \
    python3-pip \
    --no-install-recommends && \
    rm -rf /var/lib/apt/lists/*

# Install Rpi.GPIO
RUN pip3 install pigpio
RUN pip3 install requests

ENV TELEGRAF_VERSION 1.2.1
RUN wget -q https://dl.influxdata.com/telegraf/releases/telegraf_${TELEGRAF_VERSION}_armhf.deb && \
    dpkg -i telegraf_${TELEGRAF_VERSION}_armhf.deb && \
    rm -f telegraf_${TELEGRAF_VERSION}_armhf.deb*

EXPOSE 8125/udp 8092/udp 8094

COPY entrypoint.sh /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
CMD ["telegraf"]
