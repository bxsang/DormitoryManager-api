import db
from flask import request
from flask_restful import Resource
import hashlib
import jwt
import utils

class Managers(Resource):
    def get(self):
        try:
            jwt = utils.get_jwt()
            role = jwt['role']
        except Exception:
            return utils.return_auth_err()
        if role != 'admin':
            return utils.return_unauthorized()
        managers = db.Manager.query.all()
        managers_schema = db.ManagerSchema(many=True)
        return {
            'success': True,
            'result': managers_schema.dump(managers)
        }

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
        managers_to_add = []
        for manager in data:
            try_manager = db.Manager.query \
                .filter(db.Manager.username == manager['username']) \
                .one_or_none()
            if try_manager is not None:
                continue
            managers_to_add.append(db.Manager(manager['name'], manager['email'], manager['username'], default_password, 'manager'))
        return {
            'success': utils.db_insert(managers_to_add)
        }

class Manager(Resource):
    def get(self, manager_id):
        try:
            jwt = utils.get_jwt()
            role = jwt['role']
        except Exception:
            return utils.return_auth_err()
        required_roles = ['manager', 'admin']
        if role not in required_roles or jwt['role'] != 'admin' and jwt['id'] != manager_id:
            return utils.return_unauthorized()
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
