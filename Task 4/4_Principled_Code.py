import flask
import sqlite3
from flask import request

app = flask.Flask(__name__)

# Configuration
DATABASE = 'temperature.db'

def connect_db():
    return sqlite3.connect(DATABASE)

def get_temperature_for_location(latitude, longitude, date):
    try:
        conn = connect_db()
        cursor = conn.cursor()

        query = "SELECT temperature FROM temperature_data WHERE latitude = ? AND longitude = ? AND date = ?"
        cursor.execute(query, (latitude, longitude, date))
        
        temperature = cursor.fetchone()
        
        if temperature:
            return temperature[0]
        else:
            return "Temperature data not found for the given location and date."
        
    except sqlite3.Error as e:
        return f"An error occurred: {e}"
    finally:
        conn.close()

@app.route('/api/temperature_for_location', methods=['GET'])
def temperature_api():
    try:
        # CWE-20: Improper Input Validation = 1
        latitude = float(request.args.get('latitude'))
        longitude = float(request.args.get('longitude'))
        date = request.args.get('date')

        # Input validation
        if not (-90 <= latitude <= 90) or not (-180 <= longitude <= 180) or not date:
            return "Invalid input parameters.", 400
        
        temperature = get_temperature_for_location(latitude, longitude, date)
        return f"The temperature for the given location on {date} is {temperature}°C."
    
    except ValueError:
        return "Invalid input parameters.", 400

if __name__ == '__main__':
    app.run()
