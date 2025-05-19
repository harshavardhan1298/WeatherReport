import mysql.connector
from datetime import datetime

def get_db_connection():
    
    conn = mysql.connector.connect(
        host="host.docker.internal",  
        database="weatherdata",       
        user="root",                  
        password="Sree@1998",         
        port=3306                     
    )
    return conn

def create_table_if_not_exists(conn):
   
    cursor = conn.cursor()

    cursor.close()

def insert_weather_data(data):
    
    try:
        conn = get_db_connection()
        create_table_if_not_exists(conn)

        
        if "datetime" not in data:
            data["datetime"] = datetime.now()
            
       
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO weather_data.weather_report
            (city, temperature, humidity, pressure, wind_speed, description, datetime)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            data["city"],
            data["temperature"],
            data["humidity"],
            data["pressure"],
            data["wind_speed"],
            data["description"],
            data["datetime"]
        ))

        conn.commit()
        cursor.close()
        print(f"Successfully inserted weather data for {data['city']}")

    except Exception as e:
        print("Error inserting data:", e)

    finally:
        if 'conn' in locals():
            conn.close()
