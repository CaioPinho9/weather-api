import requests
import json

# link do open_weather: https://openweathermap.org/

API_KEY = "a986696369c4abe9d1f9829a158b1c8b"
COUNTRY_CODE = "BR"

def get_current_weather(city_name, uf):
  link = f"https://api.openweathermap.org/data/2.5/weather?q={city_name},{COUNTRY_CODE}&appid={API_KEY}&limit{1}"
  request = requests.get(link)
  if request.ok:
    request_json = request.json()
    temp_current = request_json['main']['temp'] - 273.15
    temp_min = request_json['main']['temp_min'] - 273.15
    temp_max = request_json['main']['temp_max'] - 273.15
    humidity = request_json['main']['humidity']
    try:
      rain = request_json['rain']["1h"]
    except:
      rain = 0
      
    current_weather = {
      "city_name": city_name,
      "uf": uf,
      "temp_current": temp_current,
      "temp_min": temp_min,
      "temp_max": temp_max,
      "humidity": humidity,
      "rain":rain
    }
    return current_weather
  
def get_forecast(city_name, uf):
  link = f"https://api.openweathermap.org/data/2.5/forecast?q={city_name},{COUNTRY_CODE}&appid={API_KEY}&limit{1}"
  request = requests.get(link)
  if request.ok:
    request_json = request.json()
    temp_current = request_json['list'][0]['main']['temp'] - 273.15
    temp_min = request_json['list'][0]['main']['temp_min'] - 273.15
    temp_max = request_json['list'][0]['main']['temp_max'] - 273.15
    humidity = request_json['list'][0]['main']['humidity']
    try:
      rain = request_json['list'][0]['rain']["1h"]
    except:
      rain = 0
      
    forecast_data = {
      "city_name": city_name,
      "uf": uf,
      "temp_current": temp_current,
      "temp_min": temp_min,
      "temp_max": temp_max,
      "humidity": humidity,
      "rain":rain
    }
    return forecast_data
  
def get_cities_Centro_Oeste():
  #IBGE API gets all cities from Centro-Oeste
  link = f"https://servicodados.ibge.gov.br/api/v1/localidades/regioes/5/municipios"
  request = requests.get(link)
  request_json = request.json()
  return request_json
  
def get_current_weather_per_city():
  request_json = get_cities_Centro_Oeste()
  response = []
  for city in request_json:
    city_name = city['nome']
    uf = city["microrregiao"]["mesorregiao"]["UF"]["nome"]
    response.append(get_current_weather(city_name, uf))
  response_json = json.dumps(response)
  return response_json

def get_current_weather_per_capital():
  capitals = dict({"Brasília": "Distrito Federal", "Campo Grande": "Mato Grosso do Sul",
                   "Cuiabá": "Mato Grosso", "Goiânia": "Goiás"})
  response = []
  for city in capitals:
    city_name = city
    uf = capitals[city]
    response.append(get_current_weather(city_name, uf))
  response_json = json.dumps(response)
  return response_json

def get_forecast_per_capital():
  capitals = dict({"Brasília": "Distrito Federal", "Campo Grande": "Mato Grosso do Sul",
                   "Cuiabá": "Mato Grosso", "Goiânia": "Goiás"})
  response = []
  for city in capitals:
    city_name = city
    uf = capitals[city]
    response.append(get_forecast(city_name, uf))
  response_json = json.dumps(response)
  return response_json

def get_forecast_per_city():
  request_json = get_cities_Centro_Oeste()
  response = []
  for city in request_json:
    city_name = city['nome']
    uf = city["microrregiao"]["mesorregiao"]["UF"]["nome"]
    response.append(get_forecast(city_name, uf))
  response_json = json.dumps(response)
  return response_json
    
def print_weather(weather_json):
  weather_data = json.loads(weather_json)
  for city in weather_data:
    print("Cidade:", city['city_name'])
    print("Estado:", city['uf'])
    print("Temperatura atual:", f"{city['temp_current']:.2f}ºC")
    print("Temperatura miníma:", f"{city['temp_min']:.2f}ºC")
    print("Temperatura máxima:", f"{city['temp_max']:.2f}ºC")
    print("Umidade", f"{city['humidity']:.2f}%")
    print("Chuva:", f"{city['rain']:.2f}mm")
    print("-----------------------------------------------------")
