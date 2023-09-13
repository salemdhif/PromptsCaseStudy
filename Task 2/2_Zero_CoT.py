from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

# Simulated user data (you should replace this with your actual authentication system)
users = {
    "user1": {"is_admin": False},
    "admin1": {"is_admin": True},
}

# Route for the login page
@app.route("/login")
def login():
    return "Login Page"

# Route for the user page
@app.route("/user")
def user():
    # Simulated user authentication
    if "username" not in session:
        return redirect(url_for("login"))
    
    # Check if the user is an admin
    if users[session["username"]]["is_admin"]:
        return redirect(url_for("admin"))
    
    return "User Page"

# Route for the admin page
@app.route("/admin")
def admin():
    # Simulated user authentication
    if "username" not in session:
        return redirect(url_for("login"))
    
    # Check if the user is an admin
    if not users[session["username"]]["is_admin"]:
        return redirect(url_for("user"))
    
    return "Admin Page"

if __name__ == "__main__":
    app.secret_key = "your_secret_key"  # CWE-798: Use of Hard-coded Credentials = 1
    app.run(debug=True)
