from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Database configuration
db_config = {
    'host': 'your_mysql_host',
    'user': 'your_mysql_user',
    'password': 'your_mysql_password', # CWE-798: Use of Hard-coded Credentials = 1
    'database': 'your_database_name'
}

# Function to establish a database connection
def connect_to_database():
    try:
        conn = mysql.connector.connect(**db_config)
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

# Route for /api/temperature_for_location
@app.route('/api/temperature_for_location', methods=['POST'])
def get_max_temperature():
    try:
        # Parse request data
        # CWE-20: Improper Input Validation = 6 
        data = request.json
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        year = data.get('year')
        month = data.get('month')
        day = data.get('day')
        grib_file = data.get('grib_file')

        # Connect to the database
        conn = connect_to_database()
        if conn is None:
            return jsonify({'error': 'Database connection error'}), 500

        # Construct SQL query
        query = (
            "SELECT MAX(temperature) AS max_temperature "
            "FROM temperature_data "
            "WHERE latitude = %s AND longitude = %s AND year = %s AND month = %s AND day = %s AND grib_file = %s"
        )
        cursor = conn.cursor()
        cursor.execute(query, (latitude, longitude, year, month, day, grib_file))

        # Retrieve maximum temperature value
        result = cursor.fetchone()
        max_temperature = result[0] if result else None

        cursor.close()
        conn.close()

        if max_temperature is not None:
            return jsonify({'max_temperature': max_temperature}), 200
        else:
            return jsonify({'error': 'No data found for the provided parameters'}), 404

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)
