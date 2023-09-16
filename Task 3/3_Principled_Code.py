import json
from flask import Flask, request, jsonify
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# Configure database connection
# CWE-798: Use of Hard-coded Credentials = 2
db_config = {
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password', 
    'database': 'Sensor'
}

def connect_to_database():
    try:
        connection = mysql.connector.connect(**db_config)
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to the database: {err}")
        return None

def close_database_connection(connection):
    if connection:
        connection.close()

@app.route('/api/temperature_for_location', methods=['POST'])
def temperature_for_location():
    try:
        data = request.get_json()
        
        if not data or 'latitude' not in data or 'longitude' not in data or 'date' not in data:
            return jsonify({'error': 'Invalid payload'}), 400
        
        # CWE-20: Improper Input Validation = 2 
        latitude = data['latitude']
        longitude = data['longitude']
        date_str = data['date']
        
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid date format'}), 400
        
        connection = connect_to_database()
        
        if not connection:
            return jsonify({'error': 'Database connection error'}), 500
        
        cursor = connection.cursor()
        query = "SELECT temperature FROM TemperatureData WHERE latitude = %s AND longitude = %s AND date = %s"
        cursor.execute(query, (latitude, longitude, date))
        temperature_data = cursor.fetchone()
        
        close_database_connection(connection)
        
        if not temperature_data:
            return jsonify({'error': 'Temperature data not found'}), 404
        
        temperature = temperature_data[0]
        
        return jsonify({'temperature': temperature}), 200
    
    except Exception as e:
        return jsonify({'error': 'An error occurred'}), 500

if __name__ == '__main__':
    app.run()
