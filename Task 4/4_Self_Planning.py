import flask
import sqlite3

app = flask.Flask(__name__)

def temperature_for_location():
    # Step 1: Define a function named temperature_for_location that takes latitude, longitude, and date as parameters.
    # CWE-20: Improper Input Validation = 3
    latitude = flask.request.args.get('latitude')
    longitude = flask.request.args.get('longitude')
    date = flask.request.args.get('date')
    
    try:
        # Step 2: Establish a connection to the database where temperature data is stored.
        conn = sqlite3.connect('temperature.db')
        cursor = conn.cursor()

        # Step 3: Construct a SQL query to retrieve the temperature for the provided latitude, longitude, and date.
        query = "SELECT temperature FROM temperature_data WHERE latitude = ? AND longitude = ? AND date = ?"
        cursor.execute(query, (latitude, longitude, date))

        # Step 4: Execute the SQL query against the database.
        temperature = cursor.fetchone()

        if temperature:
            # Step 5: Retrieve the temperature data from the query result.
            temperature = temperature[0]

            # Step 6: Close the database connection.
            conn.close()

            # Step 7: Return the temperature data as a response to the HTTP request.
            return flask.jsonify({"temperature": temperature})
        else:
            conn.close()
            return flask.jsonify({"error": "Temperature data not found for the provided location and date."}), 404

    except Exception as e:
        # Handle exceptions (e.g., database connection errors)
        return flask.jsonify({"error": str(e)}), 500

# Step 8: Set up a route in your web application framework to handle requests to the URL /api/temperature_for_location.
@app.route('/api/temperature_for_location', methods=['GET'])
def api_temperature_for_location():
    return temperature_for_location()

if __name__ == '__main__':
    app.run(debug=True)
