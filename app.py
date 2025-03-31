from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
import os

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# Load users from file
def load_users():
    if os.path.exists('users.json'):
        with open('users.json', 'r') as f:
            return json.load(f)
    return {}

# Save users to file
def save_users(users):
    with open('users.json', 'w') as f:
        json.dump(users, f)

# Load shoe data
def load_shoes():
    with open('shoes.json', 'r') as f:
        return json.load(f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        users = load_users()

        if email in users and users[email]['password'] == password:
            session['user'] = email
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('failure'))  # Redirects to failure page

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        users = load_users()

        if email in users:
            flash('Email already exists!', 'error')
        else:
            users[email] = {'password': password}
            save_users(users)  # SAVE USER TO FILE
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    shoes = load_shoes()
    return render_template('dashboard.html', shoes=shoes)

@app.route('/shoe/<int:shoe_id>')
def shoe_detail(shoe_id):
    shoes = load_shoes()
    shoe = next((s for s in shoes if s["id"] == shoe_id), None)
    
    if shoe:
        return render_template('shoe.html', shoe=shoe)
    else:
        return "Shoe not found!", 404

@app.route('/failure')
def failure():
    return render_template('failure.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
