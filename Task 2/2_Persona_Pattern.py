from flask import Flask, request, redirect

app = Flask(__name__)

# Simulating user authentication
def is_authenticated():
    # You would have your own authentication logic here
    return True  # Change to actual authentication check

def is_admin():
    # You would have your own admin check logic here
    return False  # Change to actual admin check

@app.route('/')
def index():
    if not is_authenticated():
        return redirect('/login')
    elif is_admin():
        return redirect('/admin')
    else:
        return redirect('/user')

@app.route('/login')
def login():
    if is_authenticated():
        return redirect('/')
    else:
        return "Login page"

@app.route('/user')
def user():
    if not is_authenticated():
        return redirect('/login')
    elif is_admin():
        return redirect('/admin')
    else:
        return "User page"

@app.route('/admin')
def admin():
    if not is_authenticated():
        return redirect('/login')
    elif not is_admin():
        return redirect('/user')
    else:
        return "Admin page"

if __name__ == '__main__':
    app.run()
