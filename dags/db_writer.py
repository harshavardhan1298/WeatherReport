import mysql.connector
from datetime import datetime

def get_db_connection():
    """
    Create a connection to the MySQL database

    Returns:
        connection: MySQL database connection
    """
    conn = mysql.connector.connect(
        host="host.docker.internal",  # This points to your local MySQL
        database="weatherdata",        # Your database name
        user="root",                  # Your MySQL username
        password="Sree@1998",         # Your MySQL password
        port=3306                     # Your MySQL port
    )
    return conn

def create_table_if_not_exists(conn):
    """
    Create the weather_data schema and weather_report table if they don't exist

    Args:
        conn: MySQL database connection
    """
    cursor = conn.cursor()

    # The schema and table have already been created by our setup script
    # This function is kept for compatibility, but we don't need to create anything

    cursor.close()

def insert_weather_data(data):
    """
    Insert weather data into the database

    Args:
        data (dict): Weather data including temperature, humidity, etc.
    """
    try:
        conn = get_db_connection()
        create_table_if_not_exists(conn)

        # Ensure datetime is present or use current time
        if "datetime" not in data:
            data["datetime"] = datetime.now()

        # Insert data
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
