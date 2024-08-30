from flask import request, redirect, render_template, url_for, flash, session
from flask_app import app, bcrypt
from flask_app.models.user import User

@app.route('/')
def login_reg():
    return render_template('login.html')

@app.route('/register/user', methods=['POST'])
def register():
    if not User.validate_registration(request.form):
        return redirect('/')
    
    pw_hash = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pw_hash
    }

    print("Data to save in database:", data)
    user_id = User.save(data)
    print("User ID returned after saving:", user_id)
    session['user_id'] = user_id
    return redirect('/dashboard')


@app.route('/login/user', methods=['POST'])
def login():
    data = {"email": request.form['email']}
    user = User.get_by_email(data)
    if not user:
        flash("No user found", "login")
        return redirect('/')
    
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password", "login")
        return redirect('/')
    
    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect('/')




