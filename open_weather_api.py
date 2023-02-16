import requests

from datetime import datetime
from pytz import timezone
from dao_weather import DaoWeather
from db_weather import insert

# link do open_weather: https://openweathermap.org/

API_KEY = "${{ secrets.API_KEY }}"
COUNTRY_CODE = "BR"
CAPITALS = dict({"Brasília": "Distrito Federal", "Campo Grande": "Mato Grosso do Sul",
                   "Cuiabá": "Mato Grosso", "Goiânia": "Goiás"})

def get_current_weather_city(city_name, state_name):
  link = f"https://api.openweathermap.org/data/2.5/weather?q={city_name},{COUNTRY_CODE}&appid={API_KEY}&limit{1}"
  request = requests.get(link)
  if request.ok:
    request_json = request.json()
    temp_current = request_json['main']['temp'] - 273.15
    temp_min = request_json['main']['temp_min'] - 273.15
    temp_max = request_json['main']['temp_max'] - 273.15
    humidity = request_json['main']['humidity']
    date = datetime.fromtimestamp(request_json['dt'], tz = timezone("America/Sao_Paulo")
                                  ).strftime("%Y/%m/%d %H:00:00")
    try:
      rain = request_json['rain']["1h"]
    except:
      rain = 0
      
    current_weather = DaoWeather(city_name, state_name, temp_current, 
                               temp_min, temp_max, humidity, 
                               rain, date)
    current_weather.print()
    return current_weather
  
def get_forecast_city(city_name, state_name):
  link = f"https://api.openweathermap.org/data/2.5/forecast?q={city_name},{COUNTRY_CODE}&appid={API_KEY}&limit{1}"
  request = requests.get(link)
  if request.ok:
    forecast_data = []
    request_json = request.json()
    #request_json['list'] receives a forecast for the next 5 days in 3h intervals, each "time" is one of this intervals
    for time in request_json['list']:
      temp_current = time['main']['temp'] - 273.15
      temp_min = time['main']['temp_min'] - 273.15
      temp_max = time['main']['temp_max'] - 273.15
      humidity = time['main']['humidity']
      date = time['dt_txt']
      try:
        rain = time['rain']["1h"]
      except:
        rain = 0
      
      forecast_time = DaoWeather(city_name, state_name, temp_current, 
                               temp_min, temp_max, humidity, rain, date)
      forecast_time.print()
      forecast_data.append(forecast_time)
    return forecast_data
  
def get_cities_Centro_Oeste():
  #IBGE API gets all cities from Centro-Oeste
  link = f"https://servicodados.ibge.gov.br/api/v1/localidades/regioes/5/municipios"
  request = requests.get(link)
  request_json = request.json()
  cities = dict()
  for city in request_json:
    city_name = city['nome']
    state_name = city["microrregiao"]["mesorregiao"]["UF"]["nome"]
    cities[city_name] = state_name
  return cities
  
def get_current_weather(cities):
  response = []
  for city in cities:
    city_name = city
    state_name = cities[city]
    try:
      city_weather = get_current_weather_city(city_name, state_name)
      if city_weather is not None:
        response.append(city_weather)
    except Exception:
      pass
  insert("current_weather", response)

def get_forecast(cities):
  response = []
  for city in cities:
    city_name = city
    state_name = cities[city]
    try:
      city_weather = get_forecast_city(city_name, state_name)
      if city_weather is not None:
        response = [*response, *get_forecast_city(city_name, state_name)]
    except Exception:
      pass
  insert("forecast", response)
  
def get_current_weather_per_city():
  cities = get_cities_Centro_Oeste()
  response_json = get_current_weather(cities)
  return response_json

def get_current_weather_per_capital():
  global CAPITALS
  response_json = get_current_weather(CAPITALS)
  return response_json

def get_forecast_per_city():
  cities = get_cities_Centro_Oeste()
  get_forecast(cities)
    
def get_forecast_per_capital():
  global CAPITALS
  get_forecast(CAPITALS)
  
get_forecast_per_capital()
get_current_weather_per_capital()
get_forecast_per_city()
get_current_weather_per_city()
