#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import time
import json

with open('/checks/credentials-flower-power.json') as credentials_file:
    credentials = json.load(credentials_file)

    req = requests.get('https://api-flower-power-pot.parrot.com/user/v1/authenticate',
                       data={'grant_type': 'password',
                             'username': credentials['username'],
                             'password': credentials['password'],
                             'client_id': credentials['client_id'],
                             'client_secret': credentials['client_secret'],
                             })
    response = req.json()

    # Get authorization token from response
    access_token = response['access_token']
    auth_header = {'Authorization': 'Bearer {token}'.format(token=access_token)}

    # Get locations status
    req = requests.get('https://api-flower-power-pot.parrot.com/garden/v1/status',
                       headers=auth_header)
    response = req.json()

    for loc in response['locations']:
        sensor_identifier=loc['sensor']['sensor_identifier'].replace(" ", "_")
        light=loc['light']['gauge_values']['current_value']
        fertilizer=loc['fertilizer']['gauge_values']['current_value']
        soil_moisture=loc['watering']['soil_moisture']['gauge_values']['current_value']
        air_temp=loc['air_temperature']['gauge_values']['current_value']
        battery=loc['battery']['gauge_values']['current_value']

        print('flowerpower,sensor={sensor_identifier} light={light},soil_moisture={soil_moisture},air_temp={air_temp},fertilizer={fertilizer},battery={battery}'.format(
            sensor_identifier=sensor_identifier,
            light=light if light is not None else 0,
            fertilizer=fertilizer if fertilizer is not None else 0,
            soil_moisture=soil_moisture if soil_moisture is not None else 0,
            air_temp=air_temp if air_temp is not None else 0,
            battery=battery if battery is not None else 0))
