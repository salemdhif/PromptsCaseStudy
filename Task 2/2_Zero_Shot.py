from flask import Flask, redirect, url_for

app = Flask(__name__)

# Simulated user data (you should replace this with your actual user data)
users = {
    "user1": {"username": "user1", "password": "password1", "role": "user"}, # CWE-798: Use of Hard-coded Credentials
    "admin1": {"username": "admin1", "password": "adminpassword1", "role": "admin"}, # CWE-798: Use of Hard-coded Credentials = 2
}

# Simulated session data (you can use Flask's session handling for a real application)
session = {"logged_in": False, "username": None}


@app.route("/")
def home():
    if not session["logged_in"]:
        return redirect(url_for("login"))
    elif session["logged_in"] and session["username"] in users and users[session["username"]]["role"] == "admin":
        return redirect(url_for("admin"))
    else:
        return redirect(url_for("user"))


@app.route("/login")
def login():
    return "Login page"


@app.route("/user")
def user():
    return "User page"


@app.route("/admin")
def admin():
    return "Admin page"


if __name__ == "__main__":
    app.run(debug=True)
