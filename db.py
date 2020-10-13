import hashlib
from config import db, ma

class Manager(db.Model):
    __tablename__ = 'Employees'
    id = db.Column(db.Integer, primary_key = True, autoincrement=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    username = db.Column(db.String)
    password = db.Column(db.String)
    role = db.Column(db.String)
    created_date = db.Column(db.TIMESTAMP)

    def __init__(self, name, email, username, password, role):
        self.name = name
        self.email = email
        self.username = username
        self.password = hashlib.md5(password).hexdigest()
        self.role = role

class ManagerSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'username', 'role', 'created_date')

class Student(db.Model):
    __tablename__ = 'Students'
    id = db.Column(db.String, primary_key = True)
    name = db.Column(db.String)
    password = db.Column(db.String)
    hometown = db.Column(db.String)
    nationality = db.Column(db.String)
    faculty = db.Column(db.String)
    created_date = db.Column(db.TIMESTAMP)

    def __init__(self, id, name, password, hometown, nationality, faculty):
        self.id = id
        self.name = name
        self.password = hashlib.md5(password.encode()).hexdigest()
        self.hometown = hometown
        self.nationality = nationality
        self.faculty = faculty

    def insert(self):
        db.session.add(self)
        try:
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False

    def delete(self):
        db.session.delete(self)
        try:
            db.session.commit()
            return True
        except Exception:
            db.session.rollback()
            return False

class StudentSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'hometown', 'nationality', 'faculty', 'created_date')
