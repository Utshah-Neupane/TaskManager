from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///taskManager.db"
app.config['SECRET_KEY'] = '77001f4c45bbf0c7b344c14a'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

login_manager.login_view = "login_page"
login_manager.login_message_category = "info"


from task.models import User, Task, AuditLog
from task import routes


