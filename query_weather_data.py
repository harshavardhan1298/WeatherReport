"""
Simple script to query and display weather data from MySQL
"""
import mysql.connector
from tabulate import tabulate
import pandas as pd

def get_weather_data():
    """Connect to MySQL and retrieve weather data"""
    try:
        # Connect to the MySQL database
        conn = mysql.connector.connect(
            host="localhost",
            database="weatherdata",
            user="root",
            password="Sree@1998",
            port=3306
        )

        # Create a cursor
        cursor = conn.cursor()

        # Execute the query
        cursor.execute("SELECT * FROM weather_data.weather_report")

        # Fetch all rows
        rows = cursor.fetchall()

        # Get column names (check if cursor.description is not None)
        if cursor.description:
            column_names = [desc[0] for desc in cursor.description]
        else:
            column_names = []

        # Close the cursor and connection
        cursor.close()
        conn.close()

        return column_names, rows

    except Exception as e:
        print(f"Error: {e}")
        return None, None

def display_as_table(column_names, rows):
    """Display the data as a formatted table"""
    if not rows or not column_names:
        print("No data found.")
        return

    print(tabulate(rows, headers=column_names, tablefmt="grid"))

def display_as_dataframe(column_names, rows):
    """Display the data as a pandas DataFrame"""
    if not rows or not column_names:
        print("No data found.")
        return

    df = pd.DataFrame(rows, columns=column_names)
    print(df)

    # You can also perform analysis on the DataFrame
    print("\nSummary Statistics:")
    print(df[['temperature', 'humidity', 'pressure']].describe())

    return df

if __name__ == "__main__":
    print("Fetching weather data from MySQL...")
    column_names, rows = get_weather_data()

    if column_names and rows and len(rows) > 0:
        print("\nWeather Data (Table Format):")
        display_as_table(column_names, rows)

        print("\nWeather Data (DataFrame Format):")
        df = display_as_dataframe(column_names, rows)

        # You can save the data to a CSV file
        # df.to_csv("weather_data.csv", index=False)
        # print("\nData saved to weather_data.csv")
    else:
        print("\nNo data available. Make sure the MySQL database is running and contains weather data.")
