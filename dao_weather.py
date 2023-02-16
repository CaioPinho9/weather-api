class DaoWeather:
  def  __init__(self, city_name, state_name, temp_current, 
                temp_min, temp_max, humidity, rain, date):
    self.city_name = city_name
    self.state_name = state_name
    self.date = date
    self.temp_current = temp_current
    self.temp_min = temp_min
    self.temp_max = temp_max
    self.humidity = humidity
    self.rain = rain
    
  def toDict(self):
    return {"city_name":self.city_name, "state_name":self.state_name, "date":self.date, "temp_current":self.temp_current, "temp_min":self.temp_min, "temp_max":self.temp_max, "humidity":self.humidity, "rain":self.rain}
    
  def print(self):
    print("Cidade:", self.city_name)
    print("Estado:", self.state_name)
    print("Temperatura atual:", f"{self.temp_current:.2f}ºC")
    print("Temperatura miníma:", f"{self.temp_min:.2f}ºC")
    print("Temperatura máxima:", f"{self.temp_max:.2f}ºC")
    print("Umidade", f"{self.humidity:.2f}%")
    print("Chuva:", f"{self.rain:.2f}mm")
    print("Data:", self.date)
    print("-----------------------------------------------------")
    
    