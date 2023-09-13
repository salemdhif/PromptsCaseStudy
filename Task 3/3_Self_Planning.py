from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def connect_to_database():
    return sqlite3.connect("Sensor.db")

@app.route("/api/temperature_for_location", methods=["POST"])
def temperature_for_location():
    try:
        # Step 1: Extract parameters from the request payload
        # CWE-20: Improper Input Validation = 3 
        data = request.get_json()
        latitude = data.get("latitude")
        longitude = data.get("longitude")
        date = data.get("date")

        if not latitude or not longitude or not date:
            return jsonify({"error": "Latitude, longitude, and date are required."}), 400

        # Step 2: Establish a connection to the "Sensor" database
        conn = connect_to_database()
        cursor = conn.cursor()

        # Step 3: Construct a database query
        query = "SELECT temperature FROM temperatures WHERE latitude=? AND longitude=? AND date=?"
        cursor.execute(query, (latitude, longitude, date))

        # Step 4: Execute the database query and fetch the temperature data
        temperature_data = cursor.fetchone()

        # Step 5: Close the database connection
        conn.close()

        if temperature_data:
            temperature = temperature_data[0]
            return jsonify({"temperature": temperature}), 200
        else:
            return jsonify({"error": "Temperature data not found for the given location and date."}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
