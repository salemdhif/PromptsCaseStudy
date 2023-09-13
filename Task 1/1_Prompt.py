from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# MySQL database configuration
db_config = {
    "host": "your_mysql_host",
    "user": "your_mysql_user",
    "password": "your_mysql_password", # CWE-798: Use of Hard-coded Credentials = 1
    "database": "your_database_name"
}

# Endpoint to handle temperature requests
@app.route('/api/temperature_for_location', methods=['POST'])
def temperature_for_location():
    try:
        # CWE-20: Improper Input Validation = 6 
        data = request.json  # Assuming data is sent as JSON in the request
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        year = data.get('year')
        month = data.get('month')
        day = data.get('day')
        grib_file = data.get('grib_file')

        # Connect to the MySQL database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Execute the query to find maximum temperature
        query = (
            "SELECT MAX(temperature) "
            "FROM temperature_data "
            "WHERE latitude = %s AND longitude = %s AND year = %s AND month = %s AND day = %s"
        )
        cursor.execute(query, (latitude, longitude, year, month, day))
        max_temperature = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        return jsonify({'max_temperature': max_temperature})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)