import sys
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import subprocess

def initialize_firebase():
    try:
        cred = credentials.Certificate('D:\\College Work\\ProjectWork\\Water-Level-Checker\\credentials.json')
        firebase_admin.initialize_app(cred, {'databaseURL' : 'https://water-level-checker-933ca-default-rtdb.asia-southeast1.firebasedatabase.app'})
        print("Firebase initialization successful")
    except Exception as e:
        print(f"Failed to initialize Firebase: {e}")
        sys.exit(1)

def get_database_reference():
    try:
        ref = db.reference('/Data')
        print("Database reference obtained successfully")
        return ref
    except Exception as e:
        print(f"Failed to get database reference: {e}")
        sys.exit(1)

def check_serial_number(ref, serial_number):
    try:
        snapshot = ref.order_by_child('serial_number').equal_to(serial_number).get()
        return bool(snapshot)
    except Exception as e:
        print(f"Error checking serial number: {e}")
        return False

def start_services():
    try:
        subprocess.run(["python", "Sensor_service.py"])
    except Exception as e:
        print(f"Error starting services: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python StartServices.py {Serial number}")
        sys.exit(1)

    serial_number = sys.argv[1]

    initialize_firebase()
    ref = get_database_reference()

    if check_serial_number(ref, serial_number):
        print("Serial number exists. Starting services...")
        start_services()
    else:
        print(f"Serial number {serial_number} does not exist. Please go to the website and register the machine.")
