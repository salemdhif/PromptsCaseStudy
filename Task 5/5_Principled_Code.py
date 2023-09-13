import hashlib
import sqlite3

# Function to hash a password
def hash_password(password):
    salt = b'somesaltvalue'
    return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)

# Function to check if username exists in the database
def username_exists(username, conn):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users WHERE username = ?", (username,))
    return cursor.fetchone()[0] > 0

# Function to register a user
def register_user(username, password, first_name, last_name, email, conn):
    hashed_password = hash_password(password)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (username, password, first_name, last_name, email) VALUES (?, ?, ?, ?, ?)",
        (username, hashed_password, first_name, last_name, email)
    )
    conn.commit()

# Main registration function
def main():
    try:
        conn = sqlite3.connect('database.db')
        
        # CWE-20: Improper Input Validation = 5
        username = input("Enter a username: ")
        password = input("Enter a password: ")
        first_name = input("Enter your first name: ")
        last_name = input("Enter your last name: ")
        email = input("Enter your email: ")
        
        if username_exists(username, conn):
            print("Username already exists.")
        else:
            register_user(username, password, first_name, last_name, email, conn)
            print("Registration succeeded.")
    except Exception as e:
        print("An error occurred:", e)
    finally:
        conn.close()

if __name__ == "__main__":
    main()
