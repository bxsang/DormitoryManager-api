import hashlib

from flask_sqlalchemy import model
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
        self.password = hashlib.md5(password.encode()).hexdigest()
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

class RoomArrangements(sql.Model):
    __tablename__ = 'RoomArrangements'
    id = id = sql.Column(sql.Integer, primary_key = True, autoincrement=True)
    semeter_name = sql.Column(sql.String, sql.ForeignKey('Semeters.name'))
    student_id = sql.Column(sql.String, sql.ForeignKey('Students.id'))
    room_name = sql.Column(sql.String, sql.ForeignKey('Rooms.name'))
    assigned_time = sql.Column(sql.TIMESTAMP)
    assigned_employee = sql.Column(sql.Integer, sql.ForeignKey('Employees.id'))
    semeter = sql.relationship('Semeters', backref='arrangements', lazy='joined')
    student = sql.relationship('Student', backref='arrangements', lazy='joined')
    room = sql.relationship('Rooms', backref='arrangements', lazy='joined')

    def __init__(self, semeter_name, student_id, room_name, assigned_employee):
        self.semeter_name = semeter_name
        self.student_id = student_id
        self.room_name = room_name
        self.assigned_employee = assigned_employee

class Attendance(sql.Model):
    __tablename__ = 'Attendance'
    date = sql.Column(sql.Date, primary_key=True)
    status = sql.Column(sql.Boolean, primary_key=True)
    student_id = sql.Column(sql.String, sql.ForeignKey('Students.id'), primary_key=True)
    student = sql.relationship('Student', backref='attendance', lazy='joined')

    def __init__(self, date, status, student_id):
        self.date = date
        self.status = status
        self.student_id = student_id

class Violations(sql.Model):
    __tablename__ = 'Violations'
    id = sql.Column(sql.Integer, primary_key = True, autoincrement=True)
    student_id = sql.Column(sql.String, sql.ForeignKey('Students.id'))
    semeter_name = sql.Column(sql.String, sql.ForeignKey('Semeters.name'))
    employee_id = sql.Column(sql.Integer, sql.ForeignKey('Employees.id'))
    message = sql.Column(sql.String)

    def __init__(self, student_id, semeter_name, employee_id, message):
        self.student_id = student_id
        self.semeter_name = semeter_name
        self.employee_id = employee_id
        self.message = message

class DotThuTien(sql.Model):
    __tablename__ = 'DotThuTien'
    id = sql.Column(sql.Integer, primary_key = True, autoincrement=True)
    name = sql.Column(sql.String)
    date_created = sql.Column(sql.Date)
    semeter_name = sql.Column(sql.String, sql.ForeignKey('Semeters.name'))

    def __init__(self, id, name, date_created, semeter_name):
        self.id = id
        self.name = name
        self.date_created = date_created
        self.semeter_name = semeter_name

class GiaDienNuoc(sql.Model):
    __tablename__ = 'GiaDienNuoc'
    dien = sql.Column(sql.Float, primary_key = True)
    nuoc = sql.Column(sql.Float, primary_key = True)

    def __init__(self, dien, nuoc):
        self.dien = dien
        self.nuoc = nuoc

class DienNuoc(sql.Model):
    __tablename__ = 'DienNuoc'
    id = sql.Column(sql.Integer, primary_key = True, autoincrement=True)
    room_name = sql.Column(sql.String, sql.ForeignKey('Rooms.name'))
    date = sql.Column(sql.Date)
    semeter_name = sql.Column(sql.String, sql.ForeignKey('Semeters.name'))
    water = sql.Column(sql.Integer)
    electricity = sql.Column(sql.Integer)
    dot_id = sql.Column(sql.Integer, sql.ForeignKey('DotThuTien.id'))

    def __init__(self, id, room_name, date, semeter_name, water, electricity, dot_id):
        self.id = id
        self.room_name = room_name
        self.date = date
        self.semeter_name = semeter_name
        self.water = water
        self.electricity = electricity
        self.dot_id = dot_id

class NopTien(sql.Model):
    __tablename__ = 'NopTien'
    id = sql.Column(sql.Integer, primary_key = True, autoincrement=True)
    student_id = sql.Column(sql.String, sql.ForeignKey('Students.id'))
    so_tien = sql.Column(sql.Float)
    trang_thai = sql.Column(sql.Boolean)
    dot_id = sql.Column(sql.Integer, sql.ForeignKey('DotThuTien.id'))

    def __init__(self, student_id, so_tien, trang_thai, dot_id):
        self.student_id = student_id
        self.so_tien = so_tien
        self.trang_thai = trang_thai
        self.dot_id = dot_id

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
    arrangements = ma.Nested('RoomArrangementsSchema', many=True)

class BuildingSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Building
    
    name = ma.auto_field()
    # rooms = ma.auto_field()
    rooms = ma.Nested('RoomsSchema', many=True)

class RoomsSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Rooms
        include_fk = True
    
    name = ma.auto_field()
    capacity = ma.auto_field()
    building_name = ma.auto_field()
    # building = ma.Nested('BuildingSchema', many=True)
    arrangements = ma.Nested('RoomArrangementsSchema', many=True)

class SemetersSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Semeters
    
    name = ma.auto_field()
    arrangements = ma.Nested('RoomArrangementsSchema', many=True)

class RoomArrangementsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = RoomArrangements
    
    id = ma.auto_field()
    semeter_name = ma.auto_field()
    student_id = ma.auto_field()
    room_name = ma.auto_field()
    assigned_time = ma.auto_field()
    assigned_employee = ma.auto_field()

class AttendanceSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Attendance
    
    date = ma.auto_field()
    status = ma.auto_field()
    student_id = ma.auto_field()
    student = ma.Nested('StudentSchema')

class ViolationsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Violations
    
    id = ma.auto_field()
    student_id = ma.auto_field()
    semeter_name = ma.auto_field()
    employee_id = ma.auto_field()
    message = ma.auto_field()

class DotThuTienSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DotThuTien
    
    id = ma.auto_field()
    name = ma.auto_field()
    date_created = ma.auto_field()
    semeter_name = ma.auto_field()

class GiaDienNuocSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = GiaDienNuoc
    
    dien = ma.auto_field()
    nuoc = ma.auto_field()

class DienNuocSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = DienNuoc
    
    id = ma.auto_field()
    room_name = ma.auto_field()
    date = ma.auto_field()
    semeter_name = ma.auto_field()
    water = ma.auto_field()
    electricity = ma.auto_field()
    dot_id = ma.auto_field()

class NopTienSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = NopTien
    
    id = ma.auto_field()
    student_id = ma.auto_field()
    so_tien = ma.auto_field()
    trang_thai = ma.auto_field()
    dot_id = ma.auto_field()
