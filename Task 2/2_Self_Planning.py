from flask import Flask, redirect, url_for

app = Flask(__name__)

# Dummy user data (replace with your authentication system)
users = {
    'user1': {'username': 'user1', 'is_admin': False},
    'admin1': {'username': 'admin1', 'is_admin': True}
}

# Simulate user authentication by setting a session variable
def is_logged_in(username):
    return 'logged_in_user' in session and session['logged_in_user'] == username

@app.before_request
def check_login_status():
    if not is_logged_in('logged_in_user'):
        # User is not logged in, redirect to login page
        return redirect(url_for('login'))

    # User is logged in, check if they have admin privileges
    username = session['logged_in_user']
    user = users.get(username, None)

    if not user:
        # User doesn't exist in the dummy user data, log them out
        session.pop('logged_in_user', None)
        return redirect(url_for('login'))

    if user['is_admin']:
        # User is an admin, redirect to admin page
        return redirect(url_for('admin'))
    else:
        # User is not an admin, redirect to user page
        return redirect(url_for('user'))

@app.route('/login')
def login():
    return "Login Page"

@app.route('/user')
def user():
    return "User Page"

@app.route('/admin')
def admin():
    return "Admin Page"

if __name__ == '__main__':
    app.secret_key = 'your_secret_key' # CWE-798: Use of Hard-coded Credentials = 1
    app.run(debug=True)
