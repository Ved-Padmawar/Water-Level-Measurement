import firebase_admin
from firebase_admin import credentials, db
import sys
from flask import Flask, request, redirect, render_template, session, jsonify
from addData import add_water_level_data
from fetchData import fetch_water_level_data

app = Flask(__name__, static_folder='static')
app.secret_key = '21BD1A1259C9B5'
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
        ref = db.reference('/Data')
        print("Database reference obtained successfully")
        return ref
    except Exception as e:
        print(f"Failed to get database reference: {e}")
        sys.exit(1)

initialize_firebase()
@app.route('/api/water-level', methods=['POST'])
def receive_water_level(ref):
    data = request.json
    if not data or 'water_level' not in data or 'timestamp' not in data:
        return jsonify({"error": "Invalid data"}), 400

    water_level = data['water_level']
    timestamp = data['timestamp']
    serial_number = data['serial_number']
    add_water_level_data(ref, session.get('email'), serial_number, water_level, timestamp)

def check_value_exists(ref, field_name, value_to_check):
    snapshot = ref.order_by_child(field_name).equal_to(value_to_check).get()
    return bool(snapshot)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        data = request.json
        email = data.get('email')
        username = data.get('username')
        session['email'] = email
        ref = get_database_reference()
        receive_water_level(ref)
        if check_value_exists(ref, 'email', email):
            return redirect('/dashboard')
        else:
            ref.push({'email': email, 'name' : username})
            return redirect('/dashboard')


@app.route('/dashboard')
def dashboard():
    email = session.get('email')
    return render_template('dashboard.html', email = email)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
