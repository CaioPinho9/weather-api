from flask import jsonify


class Response:
    def toJSON(list_model_weather, responseType):
        weather_dict = {"cities": []}
        for data in list_model_weather:
            city_name = data["city_name"]
            state_name = data["state_name"]
            date = data["date"]
            temp = data["temp"]
            temp_min = data["temp_min"]
            temp_max = data["temp_max"]
            humidity = data["humidity"]
            rain = data["rain"]

            if not any(
                city["city_name"] == city_name for city in weather_dict["cities"]
            ):
                cities = weather_dict["cities"]
                cities.append(
                    {
                        "city_name": city_name,
                        "state_name": state_name,
                        "dates": [],
                    }
                )
                weather_dict["cities"] = cities

            if date not in weather_dict["cities"][-1]["dates"]:
                dates = weather_dict["cities"][-1]["dates"]
                if responseType == "daily":
                    dates.append(
                        {
                            "date": date,
                            "temp": temp,
                            "temp_min": temp_min,
                            "temp_max": temp_max,
                            "humidity": humidity,
                            "rain": rain,
                        }
                    )
                else:
                    dates.append(
                        {
                            "date": date,
                            "temp": temp,
                            "humidity": humidity,
                            "rain": rain,
                        }
                    )
                weather_dict["cities"][-1]["dates"] = dates

        return jsonify(weather_dict)
