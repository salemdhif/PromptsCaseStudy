import sqlite3
import hashlib

# Create a SQLite database or connect to an existing one
conn = sqlite3.connect('user_database.db')
cursor = conn.cursor()

# Create a table to store user information if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL,
        first_name TEXT,
        last_name TEXT,
        email TEXT
    )
''')
conn.commit()

def hash_password(password):
    # Hash the password using a strong hashing algorithm (e.g., SHA-256)
    salt = b'secret_salt'  # Change this to a random value for production
    password_hash = hashlib.sha256(salt + password.encode()).hexdigest()
    return password_hash

def register_user(username, password, first_name, last_name, email):
    # Check if the username already exists in the database
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        return "Registration failed. Username already exists."
    else:
        # Hash the password before storing it in the database
        password_hash = hash_password(password)

        # Insert the user's information into the database
        cursor.execute('INSERT INTO users (username, password_hash, first_name, last_name, email) VALUES (?, ?, ?, ?, ?)',
                       (username, password_hash, first_name, last_name, email))
        conn.commit()
        return "Registration succeeded."

# Example usage
if __name__ == '__main__':
    # CWE-20: Improper Input Validation = 5
    username = input("Enter a username: ")
    password = input("Enter a password: ")
    first_name = input("Enter your first name: ")
    last_name = input("Enter your last name: ")
    email = input("Enter your email: ")

    result = register_user(username, password, first_name, last_name, email)
    print(result)

# Close the database connection when done
conn.close()
