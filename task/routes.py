from task import app, db
from flask import render_template, redirect, url_for, flash, request
from task.forms import RegisterForm, LoginForm
from flask_login import login_user, logout_user, login_required, current_user
from task.models import User, Task, AuditLog, UserRole, TaskPriority, TaskStatus

@app.route("/")
@app.route("/home")
def home_page():
    return render_template('home.html')


@app.route("/dashboard")
def dashboard_page():
    return render_template('dashboard.html')



@app.route("/register", methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(username=form.username.data,
                              email=form.email.data,
                              password=form.password.data,
                              role=UserRole(form.role.data))
        db.session.add(user_to_create)
        db.session.commit()
        
        login_user(user_to_create)
        flash(f"Account created successfully! Your are now logged in as {user_to_create.username}", category="success")
        return redirect(url_for("dashboard_page"))
    
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')
        
    return render_template('register.html', form=form)




@app.route("/login", methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        
        if attempted_user and attempted_user.check_password_correction(attempted_password = form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as {attempted_user.username}', category= 'success')
            
            return redirect(url_for('dashboard_page'))
        
        else:
            flash('Username and password are not match! Please try again!', category= 'danger')
              
    return render_template('login.html', form = form)




@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    
    return redirect(url_for("home_page"))
    
    