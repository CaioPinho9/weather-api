import requests
import os

from dotenv import load_dotenv
from model_weather import ModelWeather
from apscheduler.schedulers.blocking import BlockingScheduler

from db_weather import DbWeather

# link do open_weather: https://openweathermap.org/

load_dotenv()
API_KEY = os.getenv("API_KEY")
COUNTRY_CODE = "BR"
CAPITALS = dict(
    {
        "Brasília": "Distrito Federal",
        "Campo Grande": "Mato Grosso do Sul",
        "Cuiabá": "Mato Grosso",
        "Goiânia": "Goiás",
    }
)

db_weather = DbWeather()


def get_cities_Centro_Oeste():
    # IBGE API gets all cities from Centro-Oeste
    link = f"https://servicodados.ibge.gov.br/api/v1/localidades/regioes/5/municipios"
    request = requests.get(link)
    request_json = request.json()
    cities = dict()
    for city in request_json:
        city_name = city["nome"]
        state_name = city["microrregiao"]["mesorregiao"]["UF"]["nome"]
        cities[city_name] = state_name
    return cities


def get_forecast_city(city_name, state_name):
    link = f"https://api.openweathermap.org/data/2.5/forecast?q={city_name},{COUNTRY_CODE}&appid={API_KEY}&limit{1}"
    request = requests.get(link)
    if request.ok:
        forecast_data = []
        request_json = request.json()
        # request_json['list'] receives a forecast for the next 5 days in 3h intervals, each "time" is one of this intervals
        for time in request_json["list"]:
            date = time["dt_txt"]
            temp = time["main"]["temp"] - 273.15
            temp_min = time["main"]["temp_min"] - 273.15
            temp_max = time["main"]["temp_max"] - 273.15
            humidity = time["main"]["humidity"]
            try:
                rain = time["rain"]["3h"]
            except:
                rain = 0

            forecast_time = ModelWeather(
                city_name, state_name, date, temp, temp_min, temp_max, humidity, rain
            )
            forecast_time.print_hourly()

            forecast_data.append(forecast_time)

        return forecast_data


def insert_forecast(cities):
    for city in cities:
        city_name = city
        state_name = cities[city]

        city_weather = get_forecast_city(city_name, state_name)

        if city_weather is not None:
            db_weather.insert("forecast_hourly", city_weather)
            forecast_analysis(city_weather)
            


def get_forecast_per_city():
    try:
        cities = get_cities_Centro_Oeste()
        insert_forecast(cities)
    except Exception as e:
        raise e


def get_forecast_per_capital():
    # Testing
    global CAPITALS
    insert_forecast(CAPITALS)


def get_data_open_weather():
    get_forecast_per_city()
    scheduler = BlockingScheduler()
    scheduler.add_job(get_forecast_per_city, "interval", hours=24)
    scheduler.start()


def forecast_analysis(forecast_data):
    days = {}
    forecast_analysis = []
    for hour in forecast_data:
        forecast_day = hour.date.split(" ")[0]

        if forecast_day not in days:
            days[forecast_day] = {
                "hours_quantity": 1,
                "model_weather": ModelWeather(
                    hour.city_name,
                    hour.state_name,
                    forecast_day,
                    hour.temp,
                    hour.temp_min,
                    hour.temp_max,
                    hour.humidity,
                    hour.rain,
                ),
            }
        else:
            model_weather = days[forecast_day]["model_weather"]

            if model_weather.temp_min > hour.temp_min:
                model_weather.temp_min = hour.temp_min

            if model_weather.temp_max < hour.temp_max:
                model_weather.temp_max = hour.temp_max

            model_weather.temp += hour.temp
            model_weather.humidity += hour.humidity
            model_weather.rain += hour.rain

            days[forecast_day]["hours_quantity"] += 1

    for day in days.values():
        if day["hours_quantity"] == 8:
            day["model_weather"].temp /= 8
            day["model_weather"].humidity /= 8
            
            day["model_weather"].print_daily()

            forecast_analysis.append(day["model_weather"])

    db_weather.insert("forecast_daily", forecast_analysis)


get_data_open_weather()
