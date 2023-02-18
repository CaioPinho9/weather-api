import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()
def insert(table, weather_data):
  try:
      connection = mysql.connector.connect(
        host= os.getenv("SQL_HOST"),
        user= os.getenv("SQL_USER"),
        password= os.getenv("SQL_PASSWORD"),
        database= os.getenv("SQL_NAME")
      )
      
      cursor = connection.cursor()
      
      mySql_create_table = """
      CREATE TABLE IF NOT EXISTS {} (
        id int auto_increment primary key, 
        city_name varchar(255), 
        state_name varchar(255), 
        date datetime, 
        temp_current float, 
        temp_min float, 
        temp_max float, 
        humidity float, 
        rain float
        );"""
      
      cursor.execute(mySql_create_table.format(table))
      
      mySql_select_exists = "SELECT * FROM {} WHERE city_name = %s AND date = %s;"
      mySql_insert_query = "INSERT INTO {} (city_name, state_name, date, temp_current, temp_min, temp_max, humidity, rain) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
      mySql_update_query = "UPDATE {} SET city_name = %s, state_name = %s, date = %s, temp_current = %s, temp_min = %s, temp_max = %s, humidity = %s, rain = %s WHERE id = %s;"

      insert_values = []
      update_values = []
      for values in weather_data:
        cursor.execute(mySql_select_exists.format(table), [values.city_name, values.date])
        exists = cursor.fetchone()
        
        if exists is None:
          insert_values.append((values.city_name, values.state_name, values.date, values.temp_current, values.temp_min, values.temp_max, values.humidity, values.rain))
        else: 
          update_values.append((values.city_name, values.state_name, values.date, values.temp_current, values.temp_min, values.temp_max, values.humidity, values.rain, exists[0]))
          
      cursor.executemany(mySql_update_query.format(table), update_values)
      cursor.executemany(mySql_insert_query.format(table), insert_values)
        
      connection.commit()
      print("Data inserted successfully into MySQL table")

  except mysql.connector.Error as error:
      print("Failed to insert into MySQL table {}".format(error))

  finally:
      if connection.is_connected():
          cursor.close()
          connection.close()
          print("MySQL connection is closed")
