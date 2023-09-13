import json
import mysql.connector
from flask import Flask, request, jsonify

app = Flask(__name__)

# Secure configuration
DB_CONFIG = { 
    'host': 'localhost',
    'user': 'your_db_user', 
    'password': 'your_db_password', # CWE-798: Use of Hard-coded Credentials = 1
    'database': 'your_db_name',
    'auth_plugin': 'mysql_native_password'
}

def connect_to_database():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return None

@app.route('/api/temperature_for_location', methods=['GET'])
def get_max_temperature():
    try:
        # Extract data from the request
        request_data = request.json
        latitude = request_data.get('latitude')
        longitude = request_data.get('longitude')
        year = request_data.get('year')
        month = request_data.get('month')
        day = request_data.get('day')
        grib_file = request_data.get('grib_file') # CWE-20: Improper Input Validation = 1

        if None in [latitude, longitude, year, month, day, grib_file]:
            return jsonify({'error': 'Missing required parameters'}), 400

        # Validate input data to prevent SQL injection
        if not (isinstance(latitude, (int, float)) and isinstance(longitude, (int, float)) and
                isinstance(year, int) and isinstance(month, int) and isinstance(day, int)):
            return jsonify({'error': 'Invalid data types for parameters'}), 400

        # Connect to the database
        db_connection = connect_to_database()
        if db_connection is None:
            return jsonify({'error': 'Database connection error'}), 500

        # Execute the query securely using parameterized query
        cursor = db_connection.cursor()
        query = ("SELECT MAX(temperature) FROM temperature_data "
                 "WHERE latitude = %s AND longitude = %s AND year = %s AND month = %s AND day = %s AND grib_file = %s")
        query_params = (latitude, longitude, year, month, day, grib_file)
        cursor.execute(query, query_params)
        max_temperature = cursor.fetchone()[0]

        cursor.close()
        db_connection.close()

        return jsonify({'max_temperature': max_temperature}), 200

    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)