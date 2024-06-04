import RPi.GPIO as GPIO 
import time
import firebase_admin
from firebase_admin import credentials, db


cred = credentials.Certificate('serviceAccountKey.json')

firebase_admin.initialize_app(cred, {

    'databaseURL': 'https://porject-iot.firebaseio.com/'
})

GPIO.setmode(GPIO.BCM)
TRIG_PIN = 23
ECHO_PIN = 24

GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

TANK_HEIGHT = 230
FULL_THRESHOLD = 210
MIN_CHANGE = 1


def get_distance():
    """Measure the distance using ultrasonic sensor."""

    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)
    GPIO.output(TRIG_PIN, False)

    pulse_start = time.time()
    
    while GPIO.input(ECHO_PIN) == 0:
        pulse_start = time.time()

    while GPIO.input(ECHO_PIN) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)

    return distance

def get_water_level_percentage():
    """Calculate the water level as percentage of the tank height."""
    distance = get_distance()
    water_level = TANK_HEIGHT - distance
    percentage = (water_level / TANK_HEIGHT) * 100
    return round(percentage,2)


def update_firebase(user_id,level):
    """Update the water level in the Firebase realtime database."""

    ref = ref = db.reference(f'/users/{user_id}/water_level')
    ref.set({
        'timestamp': time.time(),
        'level': level
    })


def main():
    """Main loop to monitor water level and update Firebase on change."""
    try:
        last_level = None
        while True:
            current_level = get_water_level_percentage()
            
            if last_level is None or abs(current_level - last_level) >= MIN_CHANGE:
                user_id = "user_id"
                update_firebase(current_level)
                last_level = current_level

            print("Water Level:", current_level, "%")
            time.sleep(10) 
    finally:
        GPIO.cleanup() 
        
if __name__ == "__main__":
    main()