import sys
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import subprocess

cred = credentials.Certificate('path/to/serviceAccountKey.json')

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://your-database-url.firebaseio.com/'
})

def check_serial_number(serial_number):
    ref = db.reference('serial-numbers')

    if ref.child(serial_number).get() is not None:
        return True
    else:
        return False

def start_services():

    subprocess.run(["python", "Sensor_service.py"])

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python mycode.py {Serial number}")
        sys.exit(1)

    serial_number = sys.argv[1]

    if check_serial_number(serial_number):
        print("Serial number exists. Starting services...")
        start_services()
    else:
        print(f"Serial number {serial_number} does not exist. Please go to the website and register the machine.")
