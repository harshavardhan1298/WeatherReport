# Daily Weather Reporting Pipeline

## Stack
- OpenWeather API
- MySQL 8.0
- Apache Airflow 2.8.1
- phpMyAdmin
- Python (requests, mysql-connector)

## Quick Start

### 1. Start the Services

```bash
docker-compose up -d
```

This command starts all services:
- MySQL database
- Airflow webserver
- Airflow scheduler
- phpMyAdmin

### 2. Access the Services

- **Airflow Web UI**: http://localhost:8080
  - Username: airflow
  - Password: airflow

- **phpMyAdmin**: http://localhost:5050
  - Username: airflow
  - Password: airflow

### 3. Run the Weather DAG

1. Open the Airflow Web UI at http://localhost:8080
2. Navigate to the DAGs page
3. Find the "daily_weather_report" DAG
4. Click the "Trigger DAG" button to run it manually

## Project Structure

- **dags/**: Contains Airflow DAG files
  - `daily_weather_dag.py`: DAG for fetching and storing weather data
  - `weather_fetcher.py`: Module for fetching weather data from API
  - `db_writer.py`: Module for writing data to the database

- **logs/**: Contains Airflow logs

- **plugins/**: Contains Airflow plugins

- **Dockerfile**: Extends the Airflow image with MySQL connector

- **docker-compose.yaml**: Defines all services (MySQL, Airflow, phpMyAdmin)

## Stopping the Services

```bash
docker-compose down
```

To remove all data volumes as well:

```bash
docker-compose down -v
```

## Troubleshooting

- **Port Conflicts**: If you have port conflicts, you can change the port mappings in the `docker-compose.yaml` file.

- **Database Connection Issues**: Check the MySQL logs using `docker logs mysql`.

- **Airflow Issues**: Check the Airflow logs in the `logs` directory or using `docker logs newpro-airflow-webserver-1`.

## Manual Setup (Alternative)

1. Install requirements:

   ```bash
   pip install -r requirements.txt
