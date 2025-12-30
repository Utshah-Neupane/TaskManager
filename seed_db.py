#To check my database if it works.

from task import app, db
from task.models import User, Task, AuditLog

with app.app_context():
    
    if not User.query.filter_by(username="John").first():
        user1 = User(username="John", email="john@gmail.com", password_hash="123456", role="admin")
        db.session.add(user1)
        db.session.commit()
    
        
    test1 = User.query.filter_by(username="John").first()
    print(test1.id)
    print(test1.username)
    print(test1.email)
    print(test1.password_hash)
    print(test1.role)
    print(test1.created_at)
    
    
    
    
    task = Task.query.filter_by(title="Sample Task").first()
    if not task:
        task = Task(title="Sample Task", description="demo", status="open",
                    priority="medium", owner_id=test1.id)
        db.session.add(task)
        db.session.commit()

    print("Tasks:", [(t.id, t.title, t.status, t.owner_id) for t in Task.query.all()])
    
 
 
 
    log = AuditLog(action="seed_test", entity="task", entity_id=task.id if task else None,
                   details={"note": "seed check"}, user_id=test1.id if test1 else None)
    db.session.add(log)
    db.session.commit()

    logs = AuditLog.query.order_by(AuditLog.id.desc()).limit(5).all()
    print("Audit logs:", [(l.id, l.action, l.entity, l.entity_id, l.user_id) for l in logs])
 
 