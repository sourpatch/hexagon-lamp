#!/usr/bin/env bash

set -euo pipefail

FILENAME=${1:-main.py}

CURRENT_WIFI_SSID=$(nmcli -g 'NAME,TYPE,STATE' con | grep '802-11-wireless:activated' | head -1 | cut -d ':' -f 1)
CURRENT_WIFI_PSK=$(nmcli --show-secrets connection show "${CURRENT_WIFI_SSID}" | grep '802-11-wireless-security.psk:' | awk '{ print $2 }')

tempfile=$(mktemp)

cp "${FILENAME}" "${tempfile}"

# Update on-disk copy with real variables
sed -i "s/\$CURRENT_WIFI_SSID/$CURRENT_WIFI_SSID/g" "${tempfile}"
sed -i "s/\$CURRENT_WIFI_PSK/$CURRENT_WIFI_PSK/g" "${tempfile}"

printf "Uploading..."
ampy --port /dev/ttyUSB0 --baud 115200 put "${tempfile}"

printf "Done!\n"
ampy --port /dev/ttyUSB0 --baud 115200 run "${tempfile}"
