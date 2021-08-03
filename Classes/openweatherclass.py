# openweatherclass Python Program for Raspberry Pi 3
# Author:  Ben Calvert
# Date: August 2, 2021 v1.0.0
# Revision: 

# Import class files

import requests
import json
import pprint


# --------------Class Definitions------------------#

class OpenWeatherAPI(object):
    
    def __init__(self, apikey, zipcode='59327', imperial='imperial'):
        self.apikey = apikey
        self.zipcode = zipcode
        self.units = imperial
        baseurl = 'https://api.openweathermap.org/data/2.5/weather?'
        self.complete_url = baseurl + 'appid=' + self.apikey + '&q=' + self.zipcode + '&units=imperial'


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

        # check results

        if result['cod'] != 404 and result['message'] != 'city not found':
            pprint.pprint(result)
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

            forecast = (('For {0}, it is currently {1} with a temperature of {2}F and winds out of {3} at {4} mph.  Barometric pressure is at {5} millibars and humity of {6}%.').format(location, weather_desc, current_temp, wind_dir, wind_speed, current_pressure, current_humidity))
            return(forecast)
        else:
            return(('Error:  Weather for zipcode {0} not found.').format(self.zipcode))