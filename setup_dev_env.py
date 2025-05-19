
import subprocess
import sys

def install_requirements():
    print("Installing required packages...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    print("Done!")

if __name__ == "__main__":
    install_requirements()
