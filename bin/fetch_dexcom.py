#!/usr/bin/env python3

import os
import json
from pydexcom import Dexcom

def fetch_and_save_glucose():
    # Initialize Dexcom client
    # Note: You'll need to set these environment variables
    username = os.getenv('DEXCOM_USERNAME')
    password = os.getenv('DEXCOM_PASSWORD')
    
    if not username or not password:
        raise ValueError("DEXCOM_USERNAME and DEXCOM_PASSWORD environment variables must be set")
    
    # Create Dexcom client
    dexcom = Dexcom(username=username, password=password)
    
    # Get the latest glucose reading
    glucose_reading = dexcom.get_latest_glucose_reading()
    
    # Create a dictionary with the reading data
    reading_data = {
        'value': glucose_reading.value,
        'trend': glucose_reading.trend_arrow,
        'timestamp': glucose_reading.datetime.isoformat(),
    }
    
    # Ensure the data-exports directory exists
    os.makedirs('./data-exports', exist_ok=True)
    
    # Save to JSON file
    output_path = os.path.join('../data-exports', 'latest.json')
    with open(output_path, 'w+') as f:
        json.dump(reading_data, f, indent=2)

if __name__ == '__main__':
    fetch_and_save_glucose() 