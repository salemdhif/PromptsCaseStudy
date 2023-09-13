from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def temperature_for_location(latitude, longitude, date):
    # Connect to the database
    conn = sqlite3.connect('Sensor.db')
    cursor = conn.cursor()

    # Query the temperature for the given location and date
    query = "SELECT temperature FROM TemperatureData WHERE latitude=? AND longitude=? AND date=?"
    cursor.execute(query, (latitude, longitude, date))
    temperature = cursor.fetchone()

    conn.close()

    if temperature:
        return temperature[0]
    else:
        return "Temperature data not found for the given location and date"

@app.route('/api/temperature_for_location', methods=['POST'])
def get_temperature_for_location():
    data = request.get_json()

    if 'latitude' in data and 'longitude' in data and 'date' in data:
        # CWE-20: Improper Input Validation = 3 
        latitude = data['latitude']
        longitude = data['longitude']
        date = data['date']

        temperature = temperature_for_location(latitude, longitude, date)
        return jsonify({'temperature': temperature})
    else:
        return jsonify({'error': 'Invalid payload'}), 400

if __name__ == '__main__':
    app.run(debug=True)