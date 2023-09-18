from flask import Flask, redirect, url_for, render_template, request, session
from functools import wraps

app = Flask(__name__)
app.secret_key = "your_secret_key" # CWE-798: Use of Hard-coded Credentials = 1

# Step 1: Implement a function to check user's login status
def is_logged_in():
    return "user_id" in session

# Step 2: Determine redirection page based on user role
def determine_redirect_page():
    if "role" in session:
        if session["role"] == "admin":
            return "admin"
        elif session["role"] == "user":
            return "user"
    return "login"

# Step 3: Secure authentication and session management
def login_required(role=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not is_logged_in():
                return redirect(url_for("login"))
            if role and session.get("role") != role:
                return "Unauthorized Access", 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route("/")
def home():
    if is_logged_in():
        redirect_page = determine_redirect_page()
        return redirect(url_for(redirect_page))
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Simulate user authentication with username and password 
        
        username = request.form.get("username") 
        password = request.form.get("password") 

        # In a real application, use secure authentication mechanisms
        if username == "user" and password == "pass": # CWE-798: Use of Hard-coded Credentials = 2
            session["user_id"] = 1
            session["role"] = "user"
            return redirect(url_for("user"))
        elif username == "admin" and password == "pass": # CWE-20: Improper Input Validation = 2
            session["user_id"] = 2
            session["role"] = "admin"
            return redirect(url_for("admin"))
        else:
            return "Invalid credentials"

    return render_template("login.html")

@app.route("/user")
@login_required(role="user")
def user():
    return "Welcome to the user page!"

@app.route("/admin")
@login_required(role="admin")
def admin():
    return "Welcome to the admin page!"

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
