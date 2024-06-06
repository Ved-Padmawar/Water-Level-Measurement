from flask import Flask, request
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

app = Flask(__name__)

cred = credentials.Certificate('path/to/serviceAccountKey.json')

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://your-database-url.firebaseio.com/'
})

def check_user_exists(user_email):

    ref = db.reference('/users')

    if ref.child(user_email).get() is not None:
        return True
    else:
        return False

@app.route('/check_user', methods=['GET'])
def check_user():
    user_email = request.args.get('user_email')

    if check_user_exists(user_email):
        return f"User {user_email} exists in the database."
    
    else:
        return f"User {user_email} does not exist in the database."

if __name__ == "__main__":
    app.run(debug=True)
