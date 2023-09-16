import json
import psycopg2
from flask import Flask, request, jsonify

app = Flask(__name__)

# Database configuration
# CWE-798: Use of Hard-coded Credentials = 2
db_config = { 
    'dbname': 'your_database_name',
    'user': 'your_database_user',
    'password': 'your_database_password', 
    'host': 'your_database_host',
    'port': 'your_database_port'
}

def temperature_for_location(latitude, longitude, date):
    try:
        # Establish a connection to the database
        connection = psycopg2.connect(**db_config)
        cursor = connection.cursor()

        # Execute the query to retrieve temperature
        query = "SELECT temperature FROM temperature_data WHERE latitude = %s AND longitude = %s AND date = %s;"
        cursor.execute(query, (latitude, longitude, date))
        temperature = cursor.fetchone()

        if temperature:
            return temperature[0]
        else:
            return None

    except psycopg2.Error as e:
        # Handle database errors
        print("Database error:", e)
        return None

    finally:
        if connection:
            cursor.close()
            connection.close()

@app.route('/api/temperature_for_location', methods=['GET'])
def get_temperature_for_location():
    try:
        # CWE-20: Improper Input Validation = 3
        latitude = float(request.args.get('latitude'))
        longitude = float(request.args.get('longitude'))
        date = request.args.get('date')

        temperature = temperature_for_location(latitude, longitude, date)

        if temperature is not None:
            response = {'temperature': temperature}
        else:
            response = {'error': 'Temperature data not found'}

        return jsonify(response)

    except ValueError:
        return jsonify({'error': 'Invalid input'})

if __name__ == '__main__':
    app.run()
