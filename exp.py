from flask import Flask, render_template, request, redirect, session, url_for
from auth import register_user, validate_user
from utils import add_transaction, get_summary, get_chart_data
from db import get_connection

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change for production

@app.route('/')
def home():
    if 'user_id' in session:
        return redirect('/dashboard')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if register_user(request.form['username'], request.form['password']):
            return redirect('/')
        return "Username already exists."
    return render_template('register.html')

@app.route('/login', methods=['POST'])
def login():
    user_id = validate_user(request.form['username'], request.form['password'])
    if user_id:
        session['user_id'] = user_id
        return redirect('/dashboard')
    return "Invalid login"

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    summary = get_summary(session['user_id'])
    chart_data = get_chart_data(session['user_id'])
    return render_template('dashboard.html', summary=summary, chart_data=chart_data)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        add_transaction(session['user_id'],
                        request.form['type'],
                        request.form['category'],
                        float(request.form['amount']),
                        request.form['date'])
        return redirect('/dashboard')
    return render_template('add_transaction.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
