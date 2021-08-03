from Classes import openweatherclass as OWC
import json

with open('/etc/piviteye/openweather.conf') as apikeyfile:
    apikey = json.load(apikeyfile)['openweatherapikey']

apikeyfile.close()

try:
    x = OWC.OpenWeatherAPI(apikey, '59529')
    results = x.get_weather_data()
    print(results)
except():
    print('issue in 1st test')

try:
    y = OWC.OpenWeatherAPI(apikey, '59327')
    results = y.get_weather_data()
    print(results)
except():
    print('issue in 2nd test')