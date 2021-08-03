from Classes import openweatherclass as OWC
import json

with open('/etc/piviteye/openweather.conf') as apikeyfile:
    apikey = json.load(apikeyfile)['openweatherapikey']

apikeyfile.close()

x = OWC.OpenWeatherAPI(apikey, '59529')
results = x.get_weather_data()
print(results)
