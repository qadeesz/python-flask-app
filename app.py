from flask import Flask, render_template, flash, url_for, logging, request, redirect, session, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
import json
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///school.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    # created_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return '{"id":"'+str(self.id) + '", "username":"' + str(self.username) + '", "email":"'+str(self.email)+'",'+ '"role":"'+str(self.role)+'"}'


# Check if is admin
def is_admin(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if session['role'] == 'admin':
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrap

# Check if user logged in


def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    return wrap


@app.route('/')
def index():

    return render_template('index.html')


@app.route('/admin')
@is_logged_in
@is_admin
def admin():
    all_users = Users.query.order_by(desc(Users.id)).all()
    return render_template('admin.html', users=all_users)


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = Users.query.filter_by(
            password=password,
            email=email
        ).first()
        if user:
            session['logged_in'] = True
            session['username'] = user.username
            session['role'] = user.role
            session['user_id'] = user.id
            if session['role'] == 'admin':
                return redirect(url_for('admin'))
            else:
                return render_template('dashboard.html', user=user)

        else:
            msg = 'Invalid Login'
            return render_template('login.html', msg=msg)
    else:
        return render_template('login.html')


@app.route('/register', methods=['POST', 'GET'])
@app.route('/add-person', methods=['POST', 'GET'])
def register():

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        new_user = Users(
            username=username,
            email=email,
            password=password,
            role=role
        )
        db.session.add(new_user)
        db.session.commit()
        if request.form['redirect'] == 'admin':
            return redirect(url_for('admin'))
        else:
            return redirect('/login')
    else:
        return render_template('register.html')


@app.route('/user/delete/<int:id>')
def delete_user(id):
    user = Users.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('admin'))


@app.route('/user/get/<int:id>')
def get_user(id):
    user = Users.query.get_or_404(id)
    return user


@app.route('/search', methods=['GET', 'POST'])
def search():

    results = []
    if request.method == 'POST':
        search = request.form['search']
        if search != '':
            results = Users.query.filter(Users.username.like(search)).all()
        else:
            results = Users.query.order_by(desc(Users.id)).all()

    return render_template('admin.html', users=results)


@app.route('/profile/update/<int:id>', methods=['GET', 'POST'])
def profile_edit(id):

    user = Users.query.get_or_404(id)

    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        user.password = request.form['password']
        db.session.commit()

    return redirect(url_for('dashboard'))


@app.route('/dashboard')
@is_logged_in
def dashboard():
    user_id = session['user_id']
    user = Users.query.get_or_404(user_id)
    return render_template('dashboard.html', user=user)

# Logout
@app.route('/logout')
@is_logged_in
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.secret_key = 'secret123'
    app.run(debug=True)
