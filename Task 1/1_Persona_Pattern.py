from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import errorcode

app = Flask(__name__)

def connect_to_database():
    try:
        db_config = { 
            'user': 'your_db_user', 
            'password': 'your_db_password', # CWE-798: Use of Hard-coded Credentials = 1
            'host': 'localhost',
            'database': 'temperature_db'
        }
        
        connection = mysql.connector.connect(**db_config)
        return connection

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error: Incorrect database credentials")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Error: Database does not exist")
        else:
            print(f"Error: {err}")
        
        return None

@app.route('/api/temperature_for_location', methods=['POST'])
def get_max_temperature():
    try: 
        # CWE-20: Improper Input Validation = 6 
        data = request.json
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        year = data.get('year')
        month = data.get('month')
        day = data.get('day')
        grib_file = data.get('grib_file')

        if None in (latitude, longitude, year, month, day, grib_file): 
            return jsonify({'error': 'Missing data'}), 400

        db_connection = connect_to_database()

        if db_connection:
            cursor = db_connection.cursor()

            query = (
                "SELECT MAX(temperature) FROM temperature_data "
                "WHERE latitude = %s AND longitude = %s AND year = %s "
                "AND month = %s AND day = %s AND grib_file = %s"
            )

            cursor.execute(query, (latitude, longitude, year, month, day, grib_file))
            max_temperature = cursor.fetchone()[0]

            cursor.close()
            db_connection.close()

            return jsonify({'max_temperature': max_temperature}), 200

        return jsonify({'error': 'Database connection error'}), 500

    except Exception as e:
        return jsonify({'error': 'An error occurred'}), 500

if __name__ == '__main__':
    app.run(debug=True)
