# Weather Data Pipeline Documentation

## Project Overview

This project implements an automated data pipeline that collects weather data from an external API and stores it in a MySQL database. The pipeline is orchestrated using Apache Airflow, which schedules and monitors the data collection process.

## Architecture

The system consists of the following components:

1. **Apache Airflow**: Orchestrates the data pipeline, schedules tasks, and monitors execution
2. **MySQL Database**: Stores the collected weather data
3. **Weather API Client**: Fetches weather data from an external API
4. **Docker**: Containerizes the Airflow environment for easy deployment

## Directory Structure

```
weather-data-pipeline/
├── dags/                  # Airflow DAG definitions
│   ├── daily_weather_dag.py  # Main DAG for weather data collection
│   ├── db_writer.py          # Database interaction module
│   └── weather_fetcher.py    # Weather API client
├── logs/                  # Airflow logs
├── plugins/               # Airflow plugins
├── docker-compose.yaml    # Docker Compose configuration
├── Dockerfile             # Docker image definition
├── query_weather_data.py  # Utility script to query the database
├── README.md              # Project overview
└── requirements.txt       # Python dependencies
```

## Components

### 1. Airflow DAGs

#### daily_weather_dag.py

This is the main DAG (Directed Acyclic Graph) that defines the workflow for collecting weather data. It:

- Runs on a daily schedule
- Fetches weather data from the API
- Processes the data
- Stores it in the MySQL database

Key parameters:
- Schedule interval: Daily
- Start date: Configured in the DAG
- Retries: Configured for task failure handling

### 2. Database Structure

The weather data is stored in a MySQL database with the following structure:

- **Database**: `weatherdata`
- **Schema**: `weather_data`
- **Table**: `weather_report`

Table structure:
```sql
CREATE TABLE weather_data.weather_report (
    id INT AUTO_INCREMENT PRIMARY KEY,
    city VARCHAR(100) NOT NULL,
    temperature FLOAT NOT NULL,
    humidity FLOAT NOT NULL,
    pressure FLOAT NOT NULL,
    wind_speed FLOAT,
    description TEXT,
    datetime TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
```

### 3. Docker Configuration

The project uses Docker to containerize the Airflow environment. The configuration is defined in:

- **docker-compose.yaml**: Defines the services (Airflow webserver, scheduler, etc.)
- **Dockerfile**: Extends the base Airflow image with custom dependencies

Services:
- **airflow-webserver**: Provides the Airflow UI (accessible at http://localhost:8080)
- **airflow-scheduler**: Runs the Airflow scheduler
- **airflow-init**: Initializes the Airflow database and creates the admin user

### 4. Database Connection

The connection to the MySQL database is configured in the Airflow environment:

```yaml
AIRFLOW__CORE__SQL_ALCHEMY_CONN: mysql://root:Sree%401998@host.docker.internal:3306/weatherdata
```

This connects to:
- Host: Your local MySQL server (via host.docker.internal)
- Port: 3306
- Database: weatherdata
- Username: root
- Password: Sree@1998

### 5. Data Flow

1. The Airflow scheduler triggers the DAG based on the schedule
2. The DAG executes the weather data collection task
3. Weather data is fetched from the API
4. The data is processed and transformed
5. The data is stored in the MySQL database
6. The process repeats according to the schedule

## Setup and Installation

### Prerequisites

- Docker and Docker Compose
- MySQL server running locally
- Python 3.8+

### Installation Steps

1. Clone the repository
2. Create the MySQL database and schema:
   ```sql
   CREATE DATABASE IF NOT EXISTS weatherdata;
   CREATE SCHEMA IF NOT EXISTS weather_data;
   ```
3. Start the Airflow containers:
   ```bash
   docker-compose up -d
   ```
4. Access the Airflow UI at http://localhost:8080
   - Username: admin
   - Password: airflow

### Configuration

Key configuration files:

1. **docker-compose.yaml**: Docker services configuration
2. **dags/daily_weather_dag.py**: DAG configuration and schedule
3. **dags/db_writer.py**: Database connection parameters

## Usage

### Accessing Airflow

1. Open a web browser and navigate to http://localhost:8080
2. Log in with username "admin" and password "airflow"
3. Navigate to the DAGs page to see the available DAGs

### Running the DAG

1. In the Airflow UI, find the "daily_weather_report" DAG
2. Click the "Trigger DAG" button to run it manually
3. Monitor the execution in the Airflow UI

### Querying the Data

Use the `query_weather_data.py` script to query the data:

```bash
python query_weather_data.py
```

Or connect directly to the MySQL database:

```sql
SELECT * FROM weather_data.weather_report ORDER BY datetime DESC LIMIT 10;
```

## Troubleshooting

### Common Issues

1. **Database Connection Issues**:
   - Verify MySQL is running
   - Check the connection parameters in db_writer.py
   - Ensure the database and schema exist

2. **Airflow Container Issues**:
   - Check container logs: `docker logs newpro-airflow-webserver-1`
   - Verify port 8080 is not in use by another application

3. **DAG Not Running**:
   - Check if the DAG is paused in the Airflow UI
   - Verify the schedule interval
   - Check the Airflow scheduler logs

## Maintenance

### Backing Up Data

To back up the weather data:

```bash
mysqldump -u root -p weatherdata weather_data.weather_report > weather_data_backup.sql
```

### Updating Dependencies

If you need to update Python dependencies:

1. Update the requirements.txt file
2. Rebuild the Docker image:
   ```bash
   docker-compose build
   ```
3. Restart the containers:
   ```bash
   docker-compose down
   docker-compose up -d
   ```

## Extending the Project

### Adding New Data Sources

To add a new data source:

1. Create a new module in the dags directory
2. Implement the API client for the new data source
3. Create a new DAG or modify the existing one to include the new data source
4. Update the database schema if necessary

### Customizing the DAG Schedule

To change the DAG schedule:

1. Open dags/daily_weather_dag.py
2. Modify the schedule_interval parameter
3. Restart the Airflow scheduler

## References

- [Apache Airflow Documentation](https://airflow.apache.org/docs/)
- [MySQL Documentation](https://dev.mysql.com/doc/)
- [Docker Documentation](https://docs.docker.com/)
