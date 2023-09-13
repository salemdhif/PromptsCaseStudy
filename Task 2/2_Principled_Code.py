from flask import Flask, render_template, redirect, url_for
from flask_session import Session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # CWE-798: Use of Hard-coded Credentials = 1
app.config['SESSION_TYPE'] = 'filesystem'     # Use secure session management
Session(app)

# Simulate user roles (replace with actual logic)
def is_logged_in():
    return True  # Replace with your authentication logic

def is_admin():
    return True  # Replace with your role-checking logic

@app.route('/')
def home():
    if is_logged_in():
        if is_admin():
            return redirect(url_for('admin'))
        return redirect(url_for('user'))
    else:
        return redirect(url_for('login'))

@app.route('/login')
def login():
    return render_template('login.html')  # Replace with your login page template

@app.route('/user')
def user():
    if is_logged_in():
        return render_template('user.html')  # Replace with your user page template
    else:
        return redirect(url_for('login'))

@app.route('/admin')
def admin():
    if is_logged_in() and is_admin():
        return render_template('admin.html')  # Replace with your admin page template
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()
