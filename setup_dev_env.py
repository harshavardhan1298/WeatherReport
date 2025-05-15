"""
Setup development environment for Airflow DAGs
This script installs the required packages for local development
"""
import subprocess
import sys

def install_requirements():
    """Install required packages from requirements.txt"""
    print("Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("Done!")

if __name__ == "__main__":
    install_requirements()
