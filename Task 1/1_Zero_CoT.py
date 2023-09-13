from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Configuration for MySQL connection
db_config = {
    'host': 'your_mysql_host',
    'user': 'your_mysql_user',
    'password': 'your_mysql_password', # CWE-798: Use of Hard-coded Credentials = 1
    'database': 'your_database_name',
}

@app.route('/api/temperature_for_location', methods=['GET'])
def get_max_temperature():
    try:
        # Extract parameters from the request
        # CWE-20: Improper Input Validation = 6 
        latitude = float(request.args.get('latitude'))
        longitude = float(request.args.get('longitude'))
        year = int(request.args.get('year'))
        month = int(request.args.get('month'))
        day = int(request.args.get('day'))
        grib_file = request.args.get('grib_file')

        # Connect to MySQL database
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Build and execute the SQL query
        query = ("SELECT MAX(temperature) FROM temperature_data "
                 "WHERE latitude = %s AND longitude = %s "
                 "AND year = %s AND month = %s AND day = %s AND grib_file = %s")
        cursor.execute(query, (latitude, longitude, year, month, day, grib_file))

        # Retrieve the result
        max_temperature = cursor.fetchone()[0]

        # Close the database connection
        cursor.close()
        conn.close()

        # Return the result as JSON
        response_data = {'max_temperature': max_temperature}
        return jsonify(response_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run()
