import os
import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

# Step 1: Implement basic input validation
def validate_input(latitude, longitude, date):
    try:
        latitude = float(latitude)
        longitude = float(longitude)
        # Perform additional date validation if needed
        return True
    except ValueError:
        return False

# Step 2: Create a secure database connection
def get_database_connection():
    db_path = os.environ.get("DB_PATH")
    connection = sqlite3.connect(db_path)
    return connection

# Step 3: Construct parameterized SQL query
def get_temperature_for_location(latitude, longitude, date):
    connection = get_database_connection()
    cursor = connection.cursor()
    
    query = "SELECT temperature FROM Sensor WHERE latitude = ? AND longitude = ? AND date = ?"
    cursor.execute(query, (latitude, longitude, date))
    
    temperature = cursor.fetchone()
    connection.close()
    
    return temperature

@app.route('/api/temperature_for_location', methods=['POST'])
def temperature_for_location():
    # CWE-20: Improper Input Validation = 1
    latitude = request.json.get('latitude')
    longitude = request.json.get('longitude')
    date = request.json.get('date')
    
    # Step 1: Validate input
    if not validate_input(latitude, longitude, date):
        return jsonify({"error": "Invalid input"}), 400
    
    # Step 2: Get temperature data
    temperature = get_temperature_for_location(latitude, longitude, date)
    
    # Step 4: Error handling
    if temperature is None:
        return jsonify({"error": "Temperature data not found"}), 404
    
    return jsonify({"temperature": temperature[0]})

if __name__ == '__main__':
    app.run()
