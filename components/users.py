import db
from flask import request, after_this_request
from flask_restful import Resource
import hashlib
import jwt
from config import limiter
from flask_limiter.util import get_ipaddr
from utils import get_jwt, return_auth_err, return_unauthorized, insert_db

class ManagerList(Resource):
    decorators = [
       limiter.limit("3/minute", key_func=get_ipaddr, methods=["GET"]),
       #limiter.limit("1/3second", key_func=get_ipaddr, methods=["POST"])    # this works with your patch if I uncomment
    ]

    def get(self):
        try:
            jwt = get_jwt()
            role = jwt['role']
        except Exception:
            return return_auth_err()
        if role != 'admin':
            return return_unauthorized()
        managers = db.Manager.query.all()
        managers_schema = db.ManagerSchema(many=True)
        return {
            'success': True,
            'result': managers_schema.dump(managers)
        }

class Manager(Resource):
    def get(self, manager_id):
        try:
            jwt = get_jwt()
            role = jwt['role']
        except Exception:
            return return_auth_err()
        required_roles = ['manager', 'admin']
        if role not in required_roles or jwt['role'] != 'admin' and jwt['id'] != manager_id:
            return return_unauthorized()
        manager = db.Manager.query \
            .filter(db.Manager.id == manager_id) \
            .one_or_none()
        manager_schema = db.ManagerSchema()
        return manager_schema.dump(manager)

class ManagerLogin(Resource):
    def post(self):
        data = request.get_json()
        md5_password = hashlib.md5(data['password'].encode()).hexdigest()

        user = db.Manager.query \
            .filter(db.Manager.username == data['username']) \
            .filter(db.Manager.password == md5_password) \
            .one_or_none()
        
        if user is None:
            return {
                'success': False,
                'token': None
            }
        
        result = db.ManagerSchema().dump(user)

        encoded_jwt = jwt.encode(
            {
                'id': result['id'],
                'role': result['role']
            },
            'secret',
            algorithm='HS256'
        )
        
        # @after_this_request
        # def set_is_bar_cookie(response):
        #     response.set_cookie('token', encoded_jwt.decode('utf-8'), max_age=64800, httponly=True)
        #     return response

        return {
            'success': True,
            'user': {
                'id': result['id'],
                'name': result['name'],
                'username': result['username'],
                'role': result['role']
            },
            'token': encoded_jwt.decode('utf-8')
        }

class StudentList(Resource):
    def get(self):
        try:
            jwt = get_jwt()
            role = jwt['role']
        except Exception:
            return return_auth_err()
        required_roles = ['manager', 'admin']
        if role not in required_roles:
            return return_unauthorized()
        students = db.Student.query.all()
        students_schema = db.StudentSchema(many=True)
        return students_schema.dump(students)
    
    def post(self):
        try:
            data = request.get_json()
            jwt = get_jwt()
            role = jwt['role']
        except Exception:
            return return_auth_err()
        required_roles = ['manager', 'admin']
        if role not in required_roles:
            return return_unauthorized()
        try_student = db.Student.query \
            .filter(db.Student.id == data['id']) \
            .one_or_none()
        if try_student is not None:
            return {
                'success': False,
                'message': 'Sinh viên đã tồn tại'
            }
        student = db.Student(data['id'], data['name'], data['password'], data['hometown'], data['nationality'], data['faculty'])
        return {
            'success': student.insert()
        }

class Student(Resource):
    def get(self, student_id):
        try:
            jwt = get_jwt()
            role = jwt['role']
        except Exception:
            return return_auth_err()
        required_roles = ['manager', 'admin', 'student']
        if role not in required_roles or jwt['role'] != 'admin' and jwt['role'] != 'manager' and jwt['id'] != student_id:
            return return_unauthorized()
        student = db.Student.query \
            .filter(db.Student.id == student_id) \
            .one_or_none()
        student_schema = db.StudentSchema()
        return student_schema.dump(student)
    
    def put(self, student_id):
        try:
            data = request.get_json()
            jwt = get_jwt()
            role = jwt['role']
        except Exception:
            return return_auth_err()
        required_roles = ['manager', 'admin', 'student']
        if role not in required_roles or jwt['role'] != 'admin' and jwt['role'] != 'manager' and jwt['id'] != student_id:
            return return_unauthorized()
        student = db.Student.query \
            .filter(db.Student.id == student_id) \
            .first()
        if student is not None:
            student.id = data['id']
            student.name = data['name']
            student.password = hashlib.md5(data['password'].encode()).hexdigest()
            student.hometown = data['hometown']
            student.nationality = data['nationality']
            student.faculty = data['faculty']
            return {
                'success': student.insert()
            }
        return {
            'success': False,
            'message': 'Sinh viên không tồn tại'
        }

    def delete(self, student_id):
        try:
            jwt = get_jwt()
            role = jwt['role']
        except Exception:
            return return_auth_err()
        required_roles = ['manager', 'admin']
        if role not in required_roles:
            return return_unauthorized()
        student = db.Student.query \
            .filter(db.Student.id == student_id) \
            .first()
        if student is not None:
            return {
                'success': student.delete()
            }
        return {
            'success': False,
            'message': 'Sinh viên không tồn tại'
        }

class StudentLogin(Resource):
    def post(self):
        data = request.get_json()
        md5_password = hashlib.md5(data['password'].encode()).hexdigest()
        user = db.Student.query \
            .filter(db.Student.id == data['username']) \
            .filter(db.Student.password == md5_password) \
            .one_or_none()
        
        if user is None:
            return {
                'success': False,
                'token': None
            }
        
        result = db.StudentSchema().dump(user)

        encoded_jwt = jwt.encode(
            {
                'id': result['id'],
                'role': 'student'
            },
            'secret',
            algorithm='HS256'
        )

        return {
            'success': True,
            'user': {
                'id': result['id'],
                'name': result['name'],
                'role': 'student'
            },
            'token': encoded_jwt.decode('utf-8')
        }

class CurrentUser(Resource):
    def get(self):
        try:
            jwt = get_jwt()
            role = jwt['role']
            person_id = jwt['id']
        except Exception:
            return return_auth_err()
        if role in ['manager', 'admin']:
            manager = db.Manager.query \
                .filter(db.Manager.id == person_id) \
                .one_or_none()
            manager_schema = db.ManagerSchema()
            return manager_schema.dump(manager)
        elif role == 'student':
            student = db.Student.query \
                .filter(db.Student.id == person_id) \
                .one_or_none()
            student_schema = db.StudentSchema()
            return student_schema.dump(student)
        return None
