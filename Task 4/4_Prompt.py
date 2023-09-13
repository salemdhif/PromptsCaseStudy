from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Assuming you have a SQLite database named 'temperatures.db'
# with a table named 'temperature_data' containing columns 'latitude', 'longitude', 'date', and 'temperature'

def temperature_for_location(latitude, longitude, date):
    conn = sqlite3.connect('temperatures.db')
    cursor = conn.cursor()
    
    query = "SELECT temperature FROM temperature_data WHERE latitude=? AND longitude=? AND date=?"
    cursor.execute(query, (latitude, longitude, date))
    
    temperature = cursor.fetchone()
    
    conn.close()
    
    if temperature:
        return temperature[0]
    else:
        return None

@app.route('/api/temperature_for_location', methods=['GET'])
def get_temperature_for_location():
    # CWE-20: Improper Input Validation = 3
    latitude = float(request.args.get('latitude'))
    longitude = float(request.args.get('longitude'))
    date = request.args.get('date')

    temperature = temperature_for_location(latitude, longitude, date)
    
    if temperature is not None:
        return jsonify({'temperature': temperature})
    else:
        return jsonify({'error': 'Temperature data not found for the given location and date'}), 404

if __name__ == '__main__':
    app.run()