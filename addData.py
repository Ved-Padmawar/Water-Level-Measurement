import time
from firebase_admin import db
def add_water_level_data(ref, email, serial_number, water_level, timestamp):
    try:
        ref = db.reference('/Data')
        all_data = ref.get()
        
        user_found = False
        for key, value in all_data.items():
            if isinstance(value, dict) and value.get('email') == email:
                user_found = True
                
                devices = value.get('devices', {})
                if serial_number in devices:
                    device_data = devices[serial_number]
                    
                    # Check if device_data is a string
                    if isinstance(device_data, str):
                        # Initialize new structure
                        new_device_data = {
                            "timestamps": [timestamp],
                            "water_levels": [water_level]
                        }
                    else:
                        # Assume it's a dictionary
                        new_device_data = device_data
                        if 'timestamps' not in new_device_data:
                            new_device_data['timestamps'] = []
                        if 'water_levels' not in new_device_data:
                            new_device_data['water_levels'] = []
                        new_device_data['timestamps'].append(timestamp)
                        new_device_data['water_levels'].append(water_level)
                    
                    # Update the database
                    ref.child(key).child('devices').child(serial_number).set(new_device_data)
                    print("Water level data added successfully")
                else:
                    print(f"Serial number {serial_number} not found in devices")
                break
        
        if not user_found:
            print(f"No user found with email: {email}")
    except Exception as e:
        print(f"Error adding data: {e}")
        import traceback
        traceback.print_exc()