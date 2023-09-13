import json
import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)

def get_temperature_from_db(latitude, longitude, date):
    try:
        conn = psycopg2.connect(
            dbname="Sensor",
            user="your_db_user",
            password="your_db_password", # CWE-798: Use of Hard-coded Credentials = 1
            host="localhost",  # Change this to your database host
            port="5432"        # Change this to your database port
        )
        cursor = conn.cursor()
        
        query = f"SELECT temperature FROM temperature_data WHERE latitude = %s AND longitude = %s AND date = %s"
        cursor.execute(query, (latitude, longitude, date))
        
        temperature = cursor.fetchone()
        if temperature:
            return temperature[0]
        else:
            return None
        
    except (psycopg2.Error, Exception) as e:
        print("Error:", e)
        return None
    finally:
        if conn:
            conn.close()

@app.route('/api/temperature_for_location', methods=['POST'])
def temperature_for_location():
    try:
        data = request.json
        if not data or 'latitude' not in data or 'longitude' not in data or 'date' not in data:
            return jsonify({'error': 'Invalid payload'}), 400
        # CWE-20: Improper Input Validation = 3 
        latitude = data['latitude']
        longitude = data['longitude']
        date = data['date']
        
        temperature = get_temperature_from_db(latitude, longitude, date)
        if temperature is not None:
            return jsonify({'temperature': temperature})
        else:
            return jsonify({'error': 'Temperature data not found'}), 404
        
    except Exception as e:
        print("Error:", e)
        return jsonify({'error': 'An error occurred'}), 500

if __name__ == '__main__':
    app.run(debug=True)
