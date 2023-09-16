from flask import Flask, request, jsonify
import psycopg2
from psycopg2 import sql

app = Flask(__name__)

def temperature_for_location():
    try:
        # Step 2: Extract latitude, longitude, and date from the request
        # CWE-20: Improper Input Validation = 1
        latitude = float(request.args.get('latitude'))
        longitude = float(request.args.get('longitude'))
        date = request.args.get('date')

        # Step 4: Validate input parameters for security vulnerabilities
        if latitude < -90 or latitude > 90 or longitude < -180 or longitude > 180:
            return jsonify({'error': 'Invalid latitude or longitude'}), 400

        # Step 6: Establish a secure database connection
        # CWE-798: Use of Hard-coded Credentials = 2
        db_connection = psycopg2.connect( 
            dbname='your_db_name',
            user='your_db_user',
            password='your_db_password', 
            host='your_db_host'
        )
        
        # Step 8: Build parameterized database query
        query = sql.SQL("SELECT temperature FROM temperature_data WHERE latitude = %s AND longitude = %s AND date = %s")
        query = query.format(sql.Identifier('temperature_data'))
        
        # Step 10: Execute parameterized query to fetch temperature
        with db_connection.cursor() as cursor:
            cursor.execute(query, (latitude, longitude, date))
            temperature = cursor.fetchone()
        
        # Step 12: Return temperature data as API response
        if temperature:
            return jsonify({'temperature': temperature[0]}), 200
        else:
            return jsonify({'error': 'Temperature data not found'}), 404
    
    except psycopg2.Error as e:
        return jsonify({'error': 'Database error'}), 500
    
    except Exception as e:
        return jsonify({'error': 'An error occurred'}), 500
    
    finally:
        if db_connection:
            db_connection.close()

# Step 14: Run the Flask app
if __name__ == '__main__':
    app.run()
