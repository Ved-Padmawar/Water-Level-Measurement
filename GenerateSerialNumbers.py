import datetime

def generate_serial_number():
    now = datetime.datetime.now()
    serial_number = now.strftime('%Y%m%d%H%M%S%f')
    return serial_number