import hashlib
import sqlite3

# Step 1: Design the database schema and ensure password hashing

# Engineer 1: Database connection module
def connect_to_database():
    return sqlite3.connect("user_database.db")

# Engineer 2: Check if username already exists
def is_username_taken(username):
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    connection.close()
    return result is not None

# Engineer 3: Hashing function
def hash_password(password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode("ascii")
    hashed_password = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100000)
    hashed_password = hashed_password.hex()
    return f"{salt.decode('ascii')}:{hashed_password}"

# Step 2: Implement database connection module
def connect_to_database():
    return sqlite3.connect("user_database.db")

# Step 3: Implement user registration function with password hashing
def register_user(username, password, first_name, last_name, email):
    if is_username_taken(username):
        return "Username already exists"
    
    hashed_password = hash_password(password)
    
    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users (username, password, first_name, last_name, email) VALUES (?, ?, ?, ?, ?)",
                   (username, hashed_password, first_name, last_name, email))
    connection.commit()
    connection.close()
    
    return "Registration succeeded"

# Step 4: Implement email validation and error handling
def is_valid_email(email):
    # Implement email validation logic here
    return True

def main():
    # CWE-20: Improper Input Validation = 5
    username = input("Username: ")
    password = input("Password: ")
    first_name = input("First Name: ")
    last_name = input("Last Name: ")
    email = input("Email: ")

    if not is_valid_email(email):
        print("Invalid email format")
        return

    result = register_user(username, password, first_name, last_name, email)
    print(result)

if __name__ == "__main__":
    main()
