import hashlib
from config import sql, ma

class Manager(sql.Model):
    __tablename__ = 'Employees'
    id = sql.Column(sql.Integer, primary_key = True, autoincrement=True)
    name = sql.Column(sql.String)
    email = sql.Column(sql.String)
    username = sql.Column(sql.String)
    password = sql.Column(sql.String)
    role = sql.Column(sql.String)
    created_date = sql.Column(sql.TIMESTAMP)

    def __init__(self, name, email, username, password, role):
        self.name = name
        self.email = email
        self.username = username
        self.password = hashlib.md5(password).hexdigest()
        self.role = role

class ManagerSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'username', 'role', 'created_date')

class Student(sql.Model):
    __tablename__ = 'Students'
    id = sql.Column(sql.String, primary_key = True)
    name = sql.Column(sql.String)
    password = sql.Column(sql.String)
    hometown = sql.Column(sql.String)
    nationality = sql.Column(sql.String)
    faculty = sql.Column(sql.String)
    created_date = sql.Column(sql.TIMESTAMP)

    def __init__(self, id, name, password, hometown, nationality, faculty):
        self.id = id
        self.name = name
        self.password = hashlib.md5(password.encode()).hexdigest()
        self.hometown = hometown
        self.nationality = nationality
        self.faculty = faculty

class StudentSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'hometown', 'nationality', 'faculty', 'created_date')
