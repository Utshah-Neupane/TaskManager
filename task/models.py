from task import db
from flask_login import UserMixin
from enum import Enum
from sqlalchemy import func

    

class UserRole(str, Enum):
    ADMIN = 'admin'
    USER = 'user'
    

class TaskStatus(str, Enum):
    OPEN = 'open'
    IN_PROGRESS = 'in_progress'
    DONE = 'done'


class TaskPriority(str, Enum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'
    

    
    
class User(db.Model, UserMixin):
    __tablename__ = "users"
    
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), unique=True, nullable=False)
    email = db.Column(db.String(length=50), unique=True, nullable=False)
    password_hash = db.Column(db.String(length=60), nullable=False)
    role = db.Column(db.Enum(UserRole, name='user_role'), nullable=False, default=UserRole.USER)
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default= func.now())
    tasks = db.relationship('Task', backref='task_owner', lazy=True)
    


class Task(db.Model):
    __tablename__ = "tasks"
    
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
    
    
    
class AuditLog(db.Model):
    __tablename__ = "audit_logs"
    
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="SET NULL"), nullable=True)
    action = db.Column(db.String(100), nullable=False)     
    entity = db.Column(db.String(50), nullable=False)   
    entity_id = db.Column(db.Integer, nullable=True)
    metadata = db.Column(db.JSON, nullable=True)     
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, server_default=func.now())

    

