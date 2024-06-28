from firebase_admin import db
def fetch_water_level_data(ref, email, serial_number):
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
                    
                    if isinstance(device_data, str):
                        return [], []
                    elif isinstance(device_data, dict):
                        timestamps = device_data.get('timestamps', [])
                        water_levels = device_data.get('water_levels', [])
                        return timestamps, water_levels
                    else:
                        return [], []
                else:
                    print(f"Serial number {serial_number} not found in devices")
                break
        
        if not user_found:
            print(f"No user found with email: {email}")
        
        return [], []
    except Exception as e:
        print(f"Error fetching water level data: {e}")
        import traceback
        traceback.print_exc()
        return [], []
