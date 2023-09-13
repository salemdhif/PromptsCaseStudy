from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

# Simulating user authentication status and role (admin or not)
logged_in = False
is_admin = False

@app.route("/")
def home():
    if logged_in:
        if is_admin:
            return redirect(url_for('admin'))
        else:
            return redirect(url_for('user'))
    else:
        return redirect(url_for('login'))

@app.route("/login")
def login():
    global logged_in
    logged_in = True
    return "You have been logged in. Redirecting..."

@app.route("/user")
def user():
    return "Welcome to the user page!"

@app.route("/admin")
def admin():
    if is_admin:
        return "Welcome to the admin page!"
    else:
        return "You are not authorized to access this page."

@app.route("/logout")
def logout():
    global logged_in, is_admin
    logged_in = False
    is_admin = False
    return "You have been logged out. Redirecting..."

if __name__ == "__main__":
    app.run()