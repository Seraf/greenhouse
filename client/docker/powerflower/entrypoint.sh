#!/bin/bash
set -e

if [ -z "$REFRESH_INTERVAL" ]; then
    REFRESH_INTERVAL="15m"
fi  

while true
do
    ./bridge display
    sleep ${REFRESH_INTERVAL}
done


