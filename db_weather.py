import mysql.connector
  
def insert(table, record):
  try:
      connection = mysql.connector.connect(
        host="${{ secrets.SQL_HOST }}",
        user="${{ secrets.SQL_USER }}",
        password="${{ secrets.SQL_PASSWORD }}",
        database="db-weather"
      )
      
      cursor = connection.cursor()
      
      cursor.execute("CREATE TABLE IF NOT EXISTS "+table+" (id int auto_increment primary key, city_name varchar(255), state_name varchar(255), date datetime, temp_current float, temp_min float, temp_max float, humidity float, rain float);")
      cursor = connection.cursor()
      
      mySql_select_exists = "SELECT * FROM "+table+" WHERE city_name = %s AND date = %s;"
      mySql_insert_query = "INSERT INTO "+table+" (city_name, state_name, date, temp_current, temp_min, temp_max, humidity, rain) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
      mySql_update_query = "UPDATE "+table+" SET city_name = %s, state_name = %s, date = %s, temp_current = %s, temp_min = %s, temp_max = %s, humidity = %s, rain = %s WHERE id = %s;"

      for values in record:
        cursor.execute(mySql_select_exists, [values.city_name, values.date])
        exists = cursor.fetchone()
        cursor = connection.cursor()
        if exists is None:
          val = (values.city_name, values.state_name, values.date, values.temp_current, values.temp_min, values.temp_max, values.humidity, values.rain)
          cursor.execute(mySql_insert_query, val)
        else: 
          val = (values.city_name, values.state_name, values.date, values.temp_current, values.temp_min, values.temp_max, values.humidity, values.rain, exists[0])
          cursor.execute(mySql_update_query, val)
        connection.commit()
        print("Record inserted successfully into Laptop table")

  except mysql.connector.Error as error:
      print("Failed to insert into MySQL table {}".format(error))

  finally:
      if connection.is_connected():
          cursor.close()
          connection.close()
          print("MySQL connection is closed")
