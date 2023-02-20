class ModelWeather:
    def __init__(
        self, city_name, state_name, date, temp, temp_min, temp_max, humidity, rain
    ):
        self.city_name = city_name
        self.state_name = state_name
        self.date = date
        self.temp = temp
        self.temp_min = temp_min
        self.temp_max = temp_max
        self.humidity = humidity
        self.rain = rain

    def to_dict(self):
        return {
            "city_name": self.city_name,
            "state_name": self.state_name,
            "date": self.date,
            "temp": self.temp,
            "temp_min": self.temp_min,
            "temp_max": self.temp_max,
            "humidity": self.humidity,
            "rain": self.rain,
        }

    def print_hourly(self):
        print("City:", self.city_name)
        print("State:", self.state_name)
        print("Data:", self.date)
        print("Temperature:", f"{self.temp:.2f}ºC")
        print("Humidity", f"{self.humidity:.2f}%")
        print("Rain:", f"{self.rain:.2f}mm")
        print("-----------------------------------------------------")

    def print_daily(self):
        print("City:", self.city_name)
        print("State:", self.state_name)
        print("Data:", self.date)
        print("Average Temperature:", f"{self.temp:.2f}ºC")
        print("Minimum Temperature:", f"{self.temp:.2f}ºC")
        print("Maximum Temperature:", f"{self.temp:.2f}ºC")
        print("Humidity", f"{self.humidity:.2f}%")
        print("Rain:", f"{self.rain:.2f}mm")
        print("-----------------------------------------------------")
