#!/usr/bin/env python3

import argparse
import re
import logging
import sys
import json

from btlewrap import available_backends, BluepyBackend, GatttoolBackend, PygattBackend

from miflora.miflora_poller import MiFloraPoller, \
    MI_CONDUCTIVITY, MI_MOISTURE, MI_LIGHT, MI_TEMPERATURE, MI_BATTERY
from miflora import miflora_scanner


def valid_miflora_mac(mac, pat=re.compile(r"C4:7C:8D:[0-9A-F]{2}:[0-9A-F]{2}:[0-9A-F]{2}")):
    """Check for valid mac adresses."""
    if not pat.match(mac.upper()):
        raise argparse.ArgumentTypeError('The MAC address "{}" seems to be in the wrong format'.format(mac))
    return mac


def poll(args):
    """Poll data from the sensor."""
    backend = _get_backend(args)
    poller = MiFloraPoller(args.mac, backend)
    print("Getting data from Mi Flora")
    print("FW: {}".format(poller.firmware_version()))
    print("Name: {}".format(poller.name()))
    print("Temperature: {}".format(poller.parameter_value(MI_TEMPERATURE)))
    print("Moisture: {}".format(poller.parameter_value(MI_MOISTURE)))
    print("Light: {}".format(poller.parameter_value(MI_LIGHT)))
    print("Conductivity: {}".format(poller.parameter_value(MI_CONDUCTIVITY)))
    print("Battery: {}".format(poller.parameter_value(MI_BATTERY)))


def scan(args):
    """Scan for sensors."""
    backend = _get_backend(args)
    print(backend)
    print('Scanning for 10 seconds...')
    devices = miflora_scanner.scan(backend, 10)
    print('Found {} devices:'.format(len(devices)))
    for device in devices:
        print('  {}'.format(device))


def _get_backend(args):
    """Extract the backend class from the command line arguments."""
    if args.backend == 'gatttool':
        backend = GatttoolBackend
    elif args.backend == 'bluepy':
        backend = BluepyBackend
    elif args.backend == 'pygatt':
        backend = PygattBackend
    else:
        raise Exception('unknown backend: {}'.format(args.backend))
    return backend


def list_backends(_):
    """List all available backends."""
    backends = [b.__name__ for b in available_backends()]
    print('\n'.join(backends))


def telegraf(args):
    """Iterate on all devices defined in the file and output info in a telegraf format."""
    backend = _get_backend(args)
    with open('/checks/miflora-devices.json') as miflora_devices_file:
        devices = json.load(miflora_devices_file)

    for device in devices['devices_list']:
        valid_miflora_mac(device['mac'])
        poller = MiFloraPoller(device['mac'], backend)
        temperature = poller.parameter_value(MI_TEMPERATURE)
        moisture = poller.parameter_value(MI_MOISTURE)
        light = poller.parameter_value(MI_LIGHT)
        fertilizer = poller.parameter_value(MI_CONDUCTIVITY)
        battery = poller.parameter_value(MI_BATTERY)

        print('miflora,sensor={sensor_identifier} light={light},moisture={moisture},temperature={temperature},fertilizer={fertilizer},battery={battery}'.format(
            sensor_identifier=device['identifier'],
            light=light if light is not None else 0,
            fertilizer=fertilizer if fertilizer is not None else 0,
            moisture=moisture if moisture is not None else 0,
            temperature=temperature if temperature is not None else 0,
            battery=battery if battery is not None else 0))


def main():
    """Main function.

    Mostly parsing the command line arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--backend', choices=['gatttool', 'bluepy', 'pygatt'], default='gatttool')
    parser.add_argument('-v', '--verbose', action='store_const', const=True)
    subparsers = parser.add_subparsers(help='sub-command help', )

    parser_poll = subparsers.add_parser('poll', help='poll data from a sensor')
    parser_poll.add_argument('mac', type=valid_miflora_mac)
    parser_poll.set_defaults(func=poll)

    parser_scan = subparsers.add_parser('scan', help='scan for devices')
    parser_scan.set_defaults(func=scan)

    parser_telegraf = subparsers.add_parser('telegraf', help='telegraf outputs of all devices in configuration')
    parser_telegraf.set_defaults(func=telegraf)

    parser_scan = subparsers.add_parser('backends', help='list the available backends')
    parser_scan.set_defaults(func=list_backends)

    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    if not hasattr(args, "func"):
        parser.print_help()
        sys.exit(0)

    args.func(args)


if __name__ == '__main__':
    main()

