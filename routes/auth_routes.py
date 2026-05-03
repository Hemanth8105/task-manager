from flask import Blueprint, request, redirect, render_template, session, flash
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/')
def home():
    return render_template("login.html")

@auth.route('/signup', methods=['POST'])
def signup():
    data     = request.form
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()
    role     = data.get('role', 'member')

    # Validation
    if not username or not password:
        return render_template("login.html", error="Username and password are required.")

    if len(password) < 6:
        return render_template("login.html", error="Password must be at least 6 characters.")

    # Duplicate username check
    if User.query.filter_by(username=username).first():
        return render_template("login.html", error="Username already taken. Choose another.")

    user = User(
        username=username,
        password=generate_password_hash(password),
        role=role
    )
    db.session.add(user)
    db.session.commit()
    return redirect('/')

@auth.route('/login', methods=['POST'])
def login():
    data     = request.form
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    if not username or not password:
        return render_template("login.html", error="Please fill in all fields.")

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        session['user_id'] = user.id
        return redirect(f"/dashboard/{user.id}")

    return render_template("login.html", error="Invalid username or password.")

@auth.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@auth.route('/forgot', methods=['GET', 'POST'])
def forgot():
    if request.method == 'POST':
        username     = request.form.get('username', '').strip()
        new_password = request.form.get('password', '').strip()

        if not username or not new_password:
            return render_template("forgot.html", error="All fields are required.")

        if len(new_password) < 6:
            return render_template("forgot.html", error="Password must be at least 6 characters.")

        user = User.query.filter_by(username=username).first()
        if user:
            user.password = generate_password_hash(new_password)
            db.session.commit()
            return render_template("login.html", success="Password updated! Please sign in.")

        return render_template("forgot.html", error="Username not found.")

    return render_template("forgot.html")
