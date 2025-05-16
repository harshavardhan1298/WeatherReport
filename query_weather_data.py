"""
Simple script to query and display weather data from MySQL
"""
import mysql.connector
from tabulate import tabulate
import pandas as pd

def get_db_connection():
    """Create a connection to the MySQL database"""
    try:
        # Try localhost first (for running directly on the host)
        conn = mysql.connector.connect(
            host="localhost",
            database="weatherdata",
            user="root",
            password="Sree@1998",
            port=3306
        )
        return conn
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def get_weather_data(limit=None):
    """
    Connect to MySQL and retrieve weather data

    Args:
        limit (int, optional): Maximum number of records to retrieve. None for all records.

    Returns:
        tuple: (column_names, rows) or (None, None) if error
    """
    conn = None
    try:
        # Connect to the MySQL database
        conn = get_db_connection()
        if not conn:
            print("Failed to connect to the database.")
            return None, None

        # Create a cursor
        cursor = conn.cursor()

        # Execute the query with optional limit
        query = "SELECT * FROM weather_data.weather_report ORDER BY datetime DESC"
        if limit and isinstance(limit, int) and limit > 0:
            query += f" LIMIT {limit}"

        cursor.execute(query)

        # Fetch all rows
        rows = cursor.fetchall()

        # Get column names (check if cursor.description is not None)
        if cursor.description:
            column_names = [desc[0] for desc in cursor.description]
        else:
            column_names = []

        # Close the cursor
        cursor.close()

        return column_names, rows

    except Exception as e:
        print(f"Error querying data: {e}")
        return None, None

    finally:
        # Ensure connection is closed even if an error occurs
        if conn:
            conn.close()

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

def save_to_csv(df, filename="weather_data.csv"):
    """Save DataFrame to CSV file"""
    try:
        df.to_csv(filename, index=False)
        print(f"\nData saved to {filename}")
        return True
    except Exception as e:
        print(f"Error saving to CSV: {e}")
        return False

if __name__ == "__main__":
    print("Weather Data Query Tool")
    print("======================")

    # Ask user if they want to limit the number of records
    try:
        limit_input = input("Enter maximum number of records to retrieve (press Enter for all): ").strip()
        limit = int(limit_input) if limit_input else None
    except ValueError:
        print("Invalid input. Using no limit.")
        limit = None

    print(f"Fetching weather data from MySQL{' (limited to ' + str(limit) + ' records)' if limit else ''}...")

    column_names, rows = get_weather_data(limit)

    if column_names and rows and len(rows) > 0:
        print(f"\nFound {len(rows)} weather records.")

        print("\nWeather Data (Table Format):")
        display_as_table(column_names, rows)

        print("\nWeather Data (DataFrame Format):")
        df = display_as_dataframe(column_names, rows)

        # Ask user if they want to save to CSV
        save_option = input("\nWould you like to save the data to a CSV file? (y/n): ").strip().lower()
        if save_option == 'y':
            filename = input("Enter filename (default: weather_data.csv): ").strip()
            if not filename:
                filename = "weather_data.csv"
            save_to_csv(df, filename)
    else:
        print("\nNo data available. Please check:")
        print("1. MySQL database is running")
        print("2. Database 'weatherdata' exists")
        print("3. Schema 'weather_data' exists")
        print("4. Table 'weather_report' exists and contains data")
        print("5. Connection parameters are correct (host, user, password, port)")
