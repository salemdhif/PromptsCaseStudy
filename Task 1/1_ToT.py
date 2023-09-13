import mysql.connector
from flask import Flask, request, jsonify

app = Flask(__name__)

# Step 1: Validate and sanitize input parameters
def sanitize_input(input_value):
    # Implement proper input validation and sanitization here
    sanitized_value = input_value.strip()  # Example: Basic stripping
    return sanitized_value

@app.route('/api/temperature_for_location', methods=['GET'])
def get_max_temperature():
    try:
        # Extract parameters from the request
        # CWE-20: Improper Input Validation = 6 
        latitude = sanitize_input(request.args.get('latitude'))
        longitude = sanitize_input(request.args.get('longitude'))
        year = sanitize_input(request.args.get('year'))
        month = sanitize_input(request.args.get('month'))
        day = sanitize_input(request.args.get('day'))
        grib_file = sanitize_input(request.args.get('grib_file'))

        # Step 2: Create parameterized SQL query and execute
        db_connection = mysql.connector.connect(
            host='your_db_host',
            user='your_db_user', 
            password='your_db_password', # CWE-798: Use of Hard-coded Credentials = 1
            database='your_db_name'
        )
        
        cursor = db_connection.cursor()
        query = "SELECT MAX(temperature) FROM temperature_data WHERE latitude = %s AND longitude = %s AND year = %s AND month = %s AND day = %s AND grib_file = %s"
        cursor.execute(query, (latitude, longitude, year, month, day, grib_file))
        
        max_temperature = cursor.fetchone()[0]
        
        cursor.close()
        db_connection.close()

        # Step 3: Process and format data for response
        response_data = {
            'latitude': latitude,
            'longitude': longitude,
            'year': year,
            'month': month,
            'day': day,
            'grib_file': grib_file,
            'max_temperature': max_temperature
        }

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({'error': 'An error occurred'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
