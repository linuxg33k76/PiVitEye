# openweatherclass Python Program for Raspberry Pi 3
# Author:  Ben Calvert
# Date: August 2, 2021 v1.0.0
# Revision: 

# Import class files

import requests
import json
# import pprint


# --------------Class Definitions------------------#

class OpenWeatherAPI(object):
    '''
    OpenWeatherAPI Class:
    Inputs:  apikey - provided with user account on openweathermap.org
             location - city,state OR zipcode
             units - weather units - weather units (default is 'imperial')
             country - two character country code (defaul is US)
    '''


    def __init__(self, apikey, location='59327', units='imperial', country='US'):
        self.apikey = apikey
        self.location = location
        self.country = country
        self.units = units
        baseurl = 'https://api.openweathermap.org/data/2.5/weather?'
        self.complete_url = baseurl + 'appid=' + self.apikey + '&q=' + self.location + ',' + self.country + '&units=' + self.units


    def get_wind_direction(self, degrees):

        wd = int(degrees)

        if wd > 348.75 or wd < 11.25:
            wind_dir = 'N'
        elif wd > 11.25 and wd < 33.75:
            wind_dir = 'NNE'
        elif wd > 33.75 and wd < 56.25:
            wind_dir = 'NE'
        elif wd > 56.25 and wd < 78.75:
            wind_dir = 'ENE'
        elif wd > 78.75 and wd <101.25:
            wind_dir = 'E'
        elif wd > 101.25 and wd < 123.75:
            wind_dir = 'ESE'
        elif wd > 123.75 and wd < 146.25:
            wind_dir = 'SE'
        elif wd > 146.25 and wd < 168.75:
            wind_dir = 'SSE'
        elif wd > 168.75 and wd < 191.25:
            wind_dir = 'S'
        elif wd > 191.25 and wd < 213.75:
            wind_dir = 'SSW'
        elif wd > 213.75 and wd < 236.25:
            wind_dir = 'SW'
        elif wd > 236.25 and wd < 258.75:
            wind_dir = 'WSW'
        elif wd > 258.75 and wd < 281.25:
            wind_dir = 'W'
        elif wd > 281.25 and wd < 303.75:
            wind_dir = 'WNW'
        elif wd > 303.75 and wd < 326.25:
            wind_dir = 'NW'
        elif wd > 326.25 and wd < 348.75:
            wind_dir = 'NNW'
        else:
            wind_dir = 'Unknown'
        return wind_dir


    def get_weather_data(self):
        response = requests.get(self.complete_url)
        result = response.json()
        # pprint.pprint(result)

        # check results

        if result['cod'] != 404 and 'message' not in result:
            data = result['main']
            current_temp = data['temp']
            current_pressure = data['pressure']
            current_humidity = data['humidity']
            weather = result['weather']
            weather_desc = weather[0]['description']
            location = result['name']
            wind_direction = result['wind']['deg']
            wind_speed = result['wind']['speed']

            # Convert Degrees to Human Direction
            wind_dir = self.get_wind_direction(wind_direction)

            forecast = (('In {0}, it is currently: {1} with a temperature of: {2}F and winds out of: {3} at {4} MPH.  Barometric pressure is: {5} hPa and humidity is: {6}%.').format(location, weather_desc, current_temp, wind_dir, wind_speed, current_pressure, current_humidity))
            return(forecast)
        else:
            return(('Error:  Weather for Location: {0} not found.').format(self.location))
