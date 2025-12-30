from task import app
from flask import render_template, redirect, url_for, flash, request
from task.forms import RegisterForm
from flask_login import login_user, logout_user, login_required, current_user


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
    
    
    return render_template('register.html', form=form)



    