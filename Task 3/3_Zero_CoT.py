from flask import Flask, request, jsonify
import sqlite3  # Replace with your database library as needed

app = Flask(__name__)

def temperature_for_location(latitude, longitude, date):
    try:
        # Establish a database connection (replace with your DB connection code)
        conn = sqlite3.connect('Sensor.db')  # Replace with your actual database connection details

        # Create a cursor object
        cursor = conn.cursor()

        # Construct the SQL query to fetch temperature data
        query = "SELECT temperature FROM temperature_data WHERE latitude=? AND longitude=? AND date=?"
        cursor.execute(query, (latitude, longitude, date))

        # Fetch the temperature result
        temperature = cursor.fetchone()

        if temperature is not None:
            return temperature[0]  # Extract the temperature value from the result
        else:
            return "Temperature data not found for the given location and date."

    except Exception as e:
        return str(e)

    finally:
        conn.close()

@app.route('/api/temperature_for_location', methods=['POST'])
def get_temperature_for_location():
    try:
        # Parse payload data
        # CWE-20: Improper Input Validation = 3
        data = request.json
        latitude = data['latitude']
        longitude = data['longitude']
        date = data['date']

        # Call the temperature_for_location function to retrieve the temperature
        temperature = temperature_for_location(latitude, longitude, date)

        # Return the temperature as a JSON response
        return jsonify({'temperature': temperature})

    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
