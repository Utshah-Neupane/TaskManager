from task import db, bcrypt, login_manager
from flask_login import UserMixin
from enum import Enum
from sqlalchemy import func


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
    

class UserRole(str, Enum):
    ADMIN = 'Admin'
    USER = 'User'
    

class TaskStatus(str, Enum):
    OPEN = 'Open'
    IN_PROGRESS = 'In_progress'
    DONE = 'Done'


class TaskPriority(str, Enum):
    LOW = 'Low'
    MEDIUM = 'Medium'
    HIGH = 'High'
    

    
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), unique=True, nullable=False)
    email = db.Column(db.String(length=50), unique=True, nullable=False)
    password_hash = db.Column(db.String(length=60), nullable=False)
    role = db.Column(db.Enum(UserRole, name='user_role'), nullable=False, default=UserRole.USER)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default= func.now())
    tasks = db.relationship('Task', backref='task_owner', lazy=True)
    
    @property
    def password(self):
        return self.password
    
    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode("utf-8")
     
    def check_password_correction(self, attempted_password):
        return bcrypt.check_password_hash(self.password_hash, attempted_password)
        


class Task(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(length=50), nullable=False)
    description = db.Column(db.String(length=225))
    status = db.Column(db.Enum(TaskStatus, name='task_status'), nullable=False, default=TaskStatus.OPEN)
    priority = db.Column(db.Enum(TaskPriority, name = 'task_priority'), nullable=False, default=TaskPriority.MEDIUM)
    due_date = db.Column(db.DateTime(timezone=True), nullable=True)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now()) 
    completed_at = db.Column(db.DateTime(timezone=True), nullable=True)
    owner_id = db.Column(db.Integer(), db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"Task: {self.title}"
    
    
    
class AuditLog(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="SET NULL"), nullable=True)
    action = db.Column(db.String(100), nullable=False)     
    entity = db.Column(db.String(50), nullable=False)   
    entity_id = db.Column(db.Integer(), nullable=True)
    details = db.Column(db.JSON(), nullable=True)     
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())

    

