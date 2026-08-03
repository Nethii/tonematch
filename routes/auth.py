# routes/auth.py

from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from database.models import db, User

auth = Blueprint('auth', __name__)


# ── REGISTER ──────────────────────────────────────────────
@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.analyse_page'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm_password', '')

        if not name or not email or not password:
            flash('All fields are required', 'error')
            return render_template('register.html')

        if password != confirm:
            flash('Passwords do not match', 'error')
            return render_template('register.html')

        if len(password) < 6:
            flash('Password must be at least 6 characters', 'error')
            return render_template('register.html')

        existing = User.query.filter_by(email=email).first()
        if existing:
            flash('An account with this email already exists', 'error')
            return render_template('register.html')

        hashed_password = generate_password_hash(password)
        user = User(name=name, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        login_user(user)
        return redirect(url_for('main.analyse_page'))

    return render_template('register.html')


# ── LOGIN ─────────────────────────────────────────────────
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.analyse_page'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash('Incorrect email or password', 'error')
            return render_template('login.html')

        login_user(user)
        return redirect(url_for('main.analyse_page'))

    return render_template('login.html')


# ── LOGOUT ────────────────────────────────────────────────
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))