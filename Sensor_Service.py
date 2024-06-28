from machine import Pin, time_pulse_us
import urequests
import utime

TRIG_PIN = 23
ECHO_PIN = 24

trig = Pin(TRIG_PIN, Pin.OUT)
echo = Pin(ECHO_PIN, Pin.IN)

TANK_HEIGHT = 230
FULL_THRESHOLD = 210
MIN_CHANGE = 1

def get_distance():
    """Measure the distance using ultrasonic sensor."""
    trig.value(1)
    utime.sleep_us(10)
    trig.value(0)
    
    pulse_duration = time_pulse_us(echo, 1, 30000)  # 30ms timeout
    if pulse_duration < 0:
        return None  # Timeout occurred
    
    distance = (pulse_duration * 0.0343) / 2
    return round(distance, 2)

def get_water_level_percentage():
    """Calculate the water level as percentage of the tank height."""
    distance = get_distance()
    if distance is None:
        return None
    water_level = TANK_HEIGHT - distance
    percentage = (water_level / TANK_HEIGHT) * 100
    return round(percentage, 2)

def send_data_to_server(water_level):
    """Send water level data to backend server."""
    url = "https://your-backend-server.com/api/water-level"
    headers = {"Content-Type": "application/json"}
    data = {"water_level": water_level, "timestamp": utime.time(), "serial_number": "20240621100726267381"}
    
    try:
        response = urequests.post(url, json=data, headers=headers)
        print("Data sent. Server response:", response.text)
        response.close()
    except Exception as e:
        print("Failed to send data:", str(e))

def main():
    """Main loop to monitor water level and send data to server on change."""
    last_level = None
    while True:
        current_level = get_water_level_percentage()
        
        if current_level is not None:
            if last_level is None or abs(current_level - last_level) >= MIN_CHANGE:
                send_data_to_server(current_level)
                last_level = current_level

            print("Water Level:", current_level, "%")
        else:
            print("Failed to read sensor")
        
        utime.sleep(10)

if __name__ == "__main__":
    main()