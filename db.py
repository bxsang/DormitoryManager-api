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

class Building(sql.Model):
    __tablename__ = 'Building'
    name = sql.Column(sql.String, primary_key = True)

    def __init__(self, name):
        self.name = name

class Rooms(sql.Model):
    __tablename__ = 'Rooms'
    name = sql.Column(sql.String, primary_key = True)
    capacity = sql.Column(sql.Integer)
    building_name = sql.Column(sql.String, sql.ForeignKey('Building.name'))
    building = sql.relationship('Building', backref='rooms', lazy='joined')

    def __init__(self, name, capacity, building_name):
        self.name = name
        self.capacity = capacity
        self.building_name = building_name

class Semeters(sql.Model):
    __tablename__ = 'Semeters'
    name = sql.Column(sql.String, primary_key = True)

    def __init__(self, name):
        self.name = name

class ManagerSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Manager
    
    id = ma.auto_field()
    name = ma.auto_field()
    email = ma.auto_field()
    username = ma.auto_field()
    role = ma.auto_field()
    created_date = ma.auto_field()

class StudentSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Student
    
    id = ma.auto_field()
    name = ma.auto_field()
    hometown = ma.auto_field()
    nationality = ma.auto_field()
    faculty = ma.auto_field()
    created_date = ma.auto_field()

class BuildingSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Building
    
    name = ma.auto_field()
    rooms = ma.auto_field()

class RoomsSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Rooms
        include_fk = True
    
    name = ma.auto_field()
    capacity = ma.auto_field()
    building_name = ma.auto_field()

class SemetersSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Semeters
    
    name = ma.auto_field()
