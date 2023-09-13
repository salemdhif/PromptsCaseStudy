import sqlite3
import hashlib
from flask import Flask, request, jsonify

app = Flask(__name__)

# Create a SQLite database (you can also use a different database)
conn = sqlite3.connect('user_database.db')
cursor = conn.cursor()

# Create a table to store user data
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE,
        password TEXT,
        first_name TEXT,
        last_name TEXT,
        email TEXT
    )
''')
conn.commit()
conn.close()

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()

        # CWE-20: Improper Input Validation = 5
        username = data['username']
        password = data['password']
        first_name = data['first_name']
        last_name = data['last_name']
        email = data['email']

        # Hash the password securely using hashlib (you can use a more secure hashing library)
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        # Check if the username already exists
        conn = sqlite3.connect('user_database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username=?', (username,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            conn.close()
            return jsonify({"message": "Username already exists"}), 400

        # Insert the new user into the database
        cursor.execute('INSERT INTO users (username, password, first_name, last_name, email) VALUES (?, ?, ?, ?, ?)',
                       (username, password_hash, first_name, last_name, email))
        conn.commit()
        conn.close()

        return jsonify({"message": "Registration succeeded"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
