import firebase_admin
from firebase_admin import credentials, db
import sys
import re
from GenerateSerialNumbers import generate_serial_number

# Initialize Firebase app
def initialize_firebase():
    try:
        cred = credentials.Certificate('credentials.json')
        firebase_admin.initialize_app(cred, {'databaseURL' : 'https://water-level-checker-933ca-default-rtdb.asia-southeast1.firebasedatabase.app'})
        print("Firebase initialization successful")
    except Exception as e:
        print(f"Failed to initialize Firebase: {e}")
        sys.exit(1)

def get_database_reference():
    try:
        initialize_firebase()
        ref = db.reference('/Data')
        print("Database reference obtained successfully")
        return ref
    except Exception as e:
        print(f"Failed to get database reference: {e}")
        sys.exit(1)


def check_value_exists(ref, field_name, value_to_check):
    snapshot = ref.order_by_child(field_name).equal_to(value_to_check).get()
    return bool(snapshot)

def is_valid_email(email):
    # Define a regular expression for validating an email
    email_regex = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    return re.match(email_regex, email) is not None

def prompt_for_email():
    while True:
        email = input("Please enter your email: ")
        if is_valid_email(email):
            print(f"Valid email entered: {email}")
            return email
        else:
            print("Invalid email. Please try again.")

def main():
    email = prompt_for_email()
    ref = get_database_reference()
    if check_value_exists(ref, 'email', email):
        print("Email exists. Starting services...")
    else:
        serial_number = generate_serial_number()
        ref.push({'email': email, 'serial_number' : serial_number})
        print(f"Email {email} with serial number {serial_number} added to the database.")

main()
