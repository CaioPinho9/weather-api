import mysql.connector
import os
from dotenv import load_dotenv

from model_weather import ModelWeather


class DbWeather:
    # values: an array of model_weather objects
    def insert(self, table, values):
        try:
            self.connect()
            mySql_create_table = """
            CREATE TABLE IF NOT EXISTS {} (
              id int auto_increment primary key, 
              city_name varchar(255), 
              state_name varchar(255), 
              date datetime, 
              temp float, 
              temp_min float, 
              temp_max float, 
              humidity float, 
              rain float
            );"""

            self.execute(mySql_create_table.format(table), "")

            # TODO: (Unique Together) to avoid selecting each one:
            mySql_select_exists = "SELECT * FROM {} WHERE city_name = %s AND date = %s;"
            mySql_insert_query = "INSERT INTO {} (city_name, state_name, date, temp, temp_min, temp_max, humidity, rain) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
            mySql_update_query = "UPDATE {} SET city_name = %s, state_name = %s, date = %s, temp = %s, temp_min = %s, temp_max = %s, humidity = %s, rain = %s WHERE id = %s;"

            insert_values = []
            update_values = []

            for model_weather in values:
                self.execute(
                    mySql_select_exists.format(table),
                    [model_weather.city_name, model_weather.date],
                )
                exists = self.fetchone()

                if exists is None:
                    insert_values.append(
                        (
                            model_weather.city_name,
                            model_weather.state_name,
                            model_weather.date,
                            model_weather.temp,
                            model_weather.temp_min,
                            model_weather.temp_max,
                            model_weather.humidity,
                            model_weather.rain,
                        )
                    )
                else:
                    update_values.append(
                        (
                            model_weather.city_name,
                            model_weather.state_name,
                            model_weather.date,
                            model_weather.temp,
                            model_weather.temp_min,
                            model_weather.temp_max,
                            model_weather.humidity,
                            model_weather.rain,
                            exists[0],
                        )
                    )

            self.executemany(mySql_update_query.format(table), update_values)
            self.executemany(mySql_insert_query.format(table), insert_values)

            self.commit()
            print(
                "{} rows inserted successfully into MySQL table".format(
                    self.cursor.rowcount
                )
            )

        except Exception as e:
            raise e

        finally:
            self.close()

    def select_forecast_by_query(self, query, params):
        try:
            self.connect()

            selected = []
            for values in params:
                self.execute(query, values)
                select = self.fetchall()
                if select is not None:
                    if len(selected) > 0:
                        selected = [*selected, *select]
                    else:
                        selected = [*select]

            response = []
            for select in selected:
                model_weather = ModelWeather(
                    select[1],
                    select[2],
                    select[3].strftime("%Y-%m-%d %H:%M:%S"),
                    select[4],
                    select[5],
                    select[6],
                    select[7],
                    select[8],
                )
                response.append(model_weather.to_dict())

            print(
                "{} rows selected successfully from MySQL table".format(len(selected))
            )
            return response

        except Exception as e:
            raise e

        finally:
            self.close()

    def select_forecast_hourly_by_cities(self, request):
        query = "SELECT * FROM forecast_hourly WHERE date >= %s AND date <= %s AND city_name = %s;"
        return self.select_forecast_by_query(query, request)

    def select_forecast_hourly_by_states(self, request):
        query = "SELECT * FROM forecast_hourly WHERE date >= %s AND date <= %s AND state_name = %s;"
        return self.select_forecast_by_query(query, request)

    def select_forecast_hourly_all(self, request):
        query = "SELECT * FROM forecast_hourly WHERE date >= %s AND date <= %s;"
        return self.select_forecast_by_query(query, request)

    def select_forecast_daily_by_cities(self, request):
        query = "SELECT * FROM forecast_daily WHERE date >= %s AND date <= %s AND city_name = %s;"
        return self.select_forecast_by_query(query, request)

    def select_forecast_daily_by_states(self, request):
        query = "SELECT * FROM forecast_daily WHERE date >= %s AND date <= %s AND state_name = %s;"
        return self.select_forecast_by_query(query, request)

    def select_forecast_daily_all(self, request):
        query = "SELECT * FROM forecast_daily WHERE date >= %s AND date <= %s;"
        return self.select_forecast_by_query(query, request)

    def connect(self):
        load_dotenv()
        try:
            self.connection = mysql.connector.connect(
                host=os.getenv("SQL_HOST"),
                user=os.getenv("SQL_USER"),
                password=os.getenv("SQL_PASSWORD"),
                database=os.getenv("SQL_NAME"),
            )

            self.cursor = self.connection.cursor()

        except mysql.connector.Error as error:
            print("Failed to connect to MySQL table {}".format(error))

    def execute(self, query, values):
        self.cursor.execute(query, values)

    def executemany(self, query, values):
        self.cursor.executemany(query, values)

    def commit(self):
        self.connection.commit()

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

    def close(self):
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
