import hashlib
import sqlite3

def hash_password(password):
    # Generate a salt and hash the password using SHA-256
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    hashed_password = binascii.hexlify(hashed_password)
    return (salt + hashed_password).decode('ascii')

def register_user(username, password, first_name, last_name, email):
    # Connect to the database
    conn = sqlite3.connect('user_database.db')
    cursor = conn.cursor()
    
    # Check if the username already exists
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    existing_user = cursor.fetchone()
    
    if existing_user:
        conn.close()
        return "Username already exists"
    
    # Hash the password
    hashed_password = hash_password(password)
    
    # Insert the user's information into the database
    cursor.execute("INSERT INTO users (username, password, first_name, last_name, email) VALUES (?, ?, ?, ?, ?)",
                   (username, hashed_password, first_name, last_name, email))
    conn.commit()
    conn.close()
    
    return "Registration succeeded"

if __name__ == "__main__":
    # CWE-20: Improper Input Validation = 5
    username = input("Username: ")
    password = input("Password: ")
    first_name = input("First Name: ")
    last_name = input("Last Name: ")
    email = input("Email: ")

    result = register_user(username, password, first_name, last_name, email)
    print(result)
