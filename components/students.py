import db
from flask import request
from flask_restful import Resource
import hashlib
import jwt
import utils

class Students(Resource):
    def get(self):
        try:
            jwt = utils.get_jwt()
            role = jwt['role']
        except Exception:
            return utils.return_auth_err()
        required_roles = ['manager', 'admin']
        if role not in required_roles:
            return utils.return_unauthorized()
        students = db.Student.query.all()
        students_schema = db.StudentSchema(many=True)
        return students_schema.dump(students)
    
    def post(self):
        default_password = 'p@ssw0rd'
        try:
            data = request.get_json()
            jwt = utils.get_jwt()
            role = jwt['role']
        except Exception:
            return utils.return_auth_err()
        required_roles = ['manager', 'admin']
        if role not in required_roles:
            return utils.return_unauthorized()
        students_to_add = []
        for student in data:
            try_student = db.Student.query \
                .filter(db.Student.id == student['id']) \
                .one_or_none()
            if try_student is not None:
                continue
            students_to_add.append(db.Student(student['id'], student['name'], default_password, student['hometown'], student['nationality'], student['faculty']))
        return {
            'success': utils.db_insert(students_to_add)
        }

class Student(Resource):
    def get(self, student_id):
        try:
            jwt = utils.get_jwt()
            role = jwt['role']
        except Exception:
            return utils.return_auth_err()
        required_roles = ['manager', 'admin', 'student']
        if role not in required_roles or jwt['role'] != 'admin' and jwt['role'] != 'manager' and jwt['id'] != student_id:
            return utils.return_unauthorized()
        student = db.Student.query \
            .filter(db.Student.id == student_id) \
            .one_or_none()
        student_schema = db.StudentSchema()
        return student_schema.dump(student)
    
    def post(self, student_id):
        default_password = 'p@ssw0rd'
        try:
            data = request.get_json()
            jwt = utils.get_jwt()
            role = jwt['role']
        except Exception:
            return utils.return_auth_err()
        required_roles = ['manager', 'admin']
        if role not in required_roles:
            return utils.return_unauthorized()
        try_student = db.Student.query \
            .filter(db.Student.id == student_id) \
            .one_or_none()
        if try_student is not None:
            return {
                'success': False,
                'message': 'Sinh viên đã tồn tại'
            }
        student = db.Student(student_id, data['name'], default_password, data['hometown'], data['nationality'], data['faculty'])
        return {
            'success': utils.db_insert([student])
        }
    
    def put(self, student_id):
        try:
            data = request.get_json()
            jwt = utils.get_jwt()
            role = jwt['role']
        except Exception:
            return utils.return_auth_err()
        required_roles = ['manager', 'admin', 'student']
        if role not in required_roles or jwt['role'] != 'admin' and jwt['role'] != 'manager' and jwt['id'] != student_id:
            return utils.return_unauthorized()
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
                'success': utils.db_insert([student])
            }
        return {
            'success': False,
            'message': 'Sinh viên không tồn tại'
        }

    def delete(self, student_id):
        try:
            jwt = utils.get_jwt()
            role = jwt['role']
        except Exception:
            return utils.return_auth_err()
        required_roles = ['manager', 'admin']
        if role not in required_roles:
            return utils.return_unauthorized()
        student = db.Student.query \
            .filter(db.Student.id == student_id) \
            .first()
        if student is not None:
            return {
                'success': utils.db_delete([student])
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

class StudentArrangements(Resource):
    def get(self, student_id):
        try:
            jwt = utils.get_jwt()
            role = jwt['role']
        except Exception:
            return utils.return_auth_err()
        required_roles = ['manager', 'admin', 'student']
        if role not in required_roles or jwt['role'] != 'admin' and jwt['role'] != 'manager' and jwt['id'] != student_id:
            return utils.return_unauthorized()
        student = db.Student.query \
            .filter(db.Student.id == student_id) \
            .one_or_none()
        student_schema = db.StudentSchema()
        return student_schema.dump(student)['arrangements']
