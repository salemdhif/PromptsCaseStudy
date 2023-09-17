from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# MySQL database configuration
# CWE-798: Use of Hard-coded Credentials = 2
db_config = {
    'host': 'your_db_host',
    'user': 'your_db_user',
    'password': 'your_db_password',
    'database': 'your_db_name',
}

# Create a connection to the MySQL database
try:
    conn = mysql.connector.connect(**db_config)
except mysql.connector.Error as err:
    print(f"Error connecting to MySQL: {err}")
    exit(1)

# API endpoint to fetch maximum temperature
@app.route('/api/temperature_for_location', methods=['GET'])
def get_max_temperature():
    try:
        # Extract data from the request
        # CWE-20: Improper Input Validation = 6 
        data = request.json
        latitude = data['latitude']
        longitude = data['longitude']
        year = data['year']
        month = data['month']
        day = data['day']
        grib_file = data['grib_file']

        # Create a cursor object
        cursor = conn.cursor()

        # Execute the SQL query
        query = (
            "SELECT MAX(temperature) "
            "FROM temperature_data "
            "WHERE latitude = %s AND longitude = %s "
            "AND year = %s AND month = %s AND day = %s AND grib_file = %s"
        )
        cursor.execute(query, (latitude, longitude, year, month, day, grib_file))

        # Fetch the result
        result = cursor.fetchone()

        # Close the cursor and connection
        cursor.close()

        if result is not None:
            max_temperature = result[0]
            return jsonify({'max_temperature': max_temperature}), 200
        else:
            return jsonify({'error': 'Data not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
