# app.py
import subprocess

from flask import Flask, request
from response import Response
from db_weather import DbWeather

app = Flask(__name__)
db_weather = DbWeather()

subprocess.Popen("python src/open_weather_api.py", shell=True)


def get_forecast_data(start_date, end_date, locations, query_func):
    if isinstance(locations, str):
        locations = [locations]

    params = [(start_date, end_date, location) for location in locations]
    weather_forecast = query_func(params)
    return Response.toJSON(weather_forecast), 200


@app.get("/forecast_hourly")
def forecast_hourly():
    if request.is_json:
        try:
            start_date = request.json["start_date"]
            end_date = request.json.get("end_date", [])
            cities = request.json.get("cities", [])
            states = request.json.get("states", [])
        except KeyError:
            return {"error": "Missing required parameter"}, 400

        if not end_date:
            end_date = start_date

        if cities:
            if type(cities) == str:
                cities = [cities]
            params = [(start_date, end_date, city_name) for city_name in cities]
            list_model_weather = db_weather.select_forecast_hourly_by_cities(params)
            return Response.toJSON(list_model_weather, "hourly"), 200
        elif states:
            if type(states) == str:
                states = [states]
            params = [(start_date, end_date, state_name) for state_name in states]
            list_model_weather = db_weather.select_forecast_hourly_by_states(params)
            return Response.toJSON(list_model_weather, "hourly"), 200
        else:
            params = [(start_date, end_date)]
            list_model_weather = db_weather.select_forecast_hourly_all(params)
            return Response.toJSON(list_model_weather, "hourly"), 200
    else:
        return {"error": "Request must be JSON"}, 415


@app.get("/forecast_daily")
def forecast_daily():
    if request.is_json:
        try:
            start_date = request.json["start_date"]
            end_date = request.json.get("end_date", [])
            cities = request.json.get("cities", [])
            states = request.json.get("states", [])
        except KeyError:
            return {"error": "Missing required parameter"}, 400

        if not end_date:
            end_date = start_date

        if cities:
            if type(cities) == str:
                cities = [cities]
            params = [(start_date, end_date, city_name) for city_name in cities]
            list_model_weather = db_weather.select_forecast_daily_by_cities(params)
            return Response.toJSON(list_model_weather, "daily"), 200
        elif states:
            if type(states) == str:
                states = [states]
            params = [(start_date, end_date, state_name) for state_name in states]
            list_model_weather = db_weather.select_forecast_daily_by_states(params)
            return Response.toJSON(list_model_weather, "daily"), 200
        else:
            params = [(start_date, end_date)]
            list_model_weather = db_weather.select_forecast_daily_all(params)
            return Response.toJSON(list_model_weather, "daily"), 200
    else:
        return {"error": "Request must be JSON"}, 415
