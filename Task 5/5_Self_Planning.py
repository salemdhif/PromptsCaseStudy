import sqlite3
import hashlib

# Function to hash passwords using SHA-256
def hash_password(password):
    salt = b'YourSecretSaltHere'  # Change this to a secure random salt
    return hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)

# Function to check if a username exists in the database
def is_username_exists(username):
    conn = sqlite3.connect('user_database.db')  # Change to your database connection
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# Function to insert a new user into the database
def insert_user(username, hashed_password):
    conn = sqlite3.connect('user_database.db')  # Change to your database connection
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
    conn.commit()
    conn.close()

# Accept user input
# CWE-20: Improper Input Validation = 5
username = input("Enter your username: ")
password = input("Enter your password: ")
first_name = input("Enter your first name: ")
last_name = input("Enter your last name: ")
email = input("Enter your email: ")

# Check if the username already exists
if is_username_exists(username):
    print("Username already exists. Please choose a different username.")
else:
    # Hash the password
    hashed_password = hash_password(password)

    # Insert the user into the database
    insert_user(username, hashed_password)

    print("Registration successful. Welcome, {}!".format(username))
