from task import app, db
from flask import render_template, redirect, url_for, flash, request
from task.forms import RegisterForm
from flask_login import login_user, logout_user, login_required, current_user
from task.models import User, Task, AuditLog, UserRole, TaskPriority, TaskStatus

@app.route("/")
@app.route("/home")
def home_page():
    return "Hello World"


@app.route("/dashboard")
def dashboard_page():
    return render_template('base.html')



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




@app.route("/login")
def login_page():
    return render_template('login.html')
    