#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import time
import json

with open('/checks/credentials-openweather.json') as credentials_file:
    credentials = json.load(credentials_file)

    req = requests.get('http://api.openweathermap.org/data/2.5/weather',
                       params={'id': credentials['city_id'],
                               'APPID': credentials['api_key'],
                               'units': credentials['units'],
                               'lang': credentials['lang']})
    response = req.json()
    
    temperature = response['main']['temp']
    pressure = response['main']['pressure']
    humidity = response['main']['humidity']
    clouds = response['clouds']['all']

    print('openweathermap temperature={temperature},pressure={pressure},humidity={humidity},clouds={clouds}'.format(
        temperature=temperature if temperature is not None else 0,
        pressure=pressure if pressure is not None else 0,
        humidity=humidity if humidity is not None else 0,
        clouds=clouds if clouds is not None else 0))
