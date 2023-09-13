import sqlite3
import hashlib

# Function to hash the password
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Function to check if a username already exists in the database
def username_exists(username):
    conn = sqlite3.connect("user_database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    result = cursor.fetchone()
    conn.close()
    return result is not None

# Function to register a new user
def register_user(username, password, first_name, last_name, email):
    conn = sqlite3.connect("user_database.db")
    cursor = conn.cursor()
    
    if username_exists(username):
        conn.close()
        return "Username already exists."
    
    hashed_password = hash_password(password)
    cursor.execute("INSERT INTO users (username, password, first_name, last_name, email) VALUES (?, ?, ?, ?, ?)",
                   (username, hashed_password, first_name, last_name, email))
    
    conn.commit()
    conn.close()
    return "Registration succeeded."

# Main function to get user input and initiate registration
def main():
    # CWE-20: Improper Input Validation = 5
    username = input("Enter username: ")
    password = input("Enter password: ")
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    email = input("Enter email: ")
    
    result = register_user(username, password, first_name, last_name, email)
    print(result)

if __name__ == "__main__":
    main()