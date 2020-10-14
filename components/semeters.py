import db
from flask import request
from flask_restful import Resource
import utils

class Semeters(Resource):
    def get(self):
        try:
            jwt = utils.get_jwt()
            role = jwt['role']
        except Exception:
            return utils.return_auth_err()
        required_roles = ['manager', 'admin']
        if role not in required_roles:
            return utils.return_unauthorized()
        semeters = db.Semeters.query.all()
        semeters_schema = db.SemetersSchema(many=True)
        return semeters_schema.dump(semeters)
    
    def post(self):
        try:
            data = request.get_json()
            jwt = utils.get_jwt()
            role = jwt['role']
        except Exception:
            return utils.return_auth_err()
        required_roles = ['manager', 'admin']
        if role not in required_roles:
            return utils.return_unauthorized()
        semeters_to_add = []
        for semeter in data:
            try_semeter = db.Semeters.query \
                .filter(db.Semeters.name == semeter['name']) \
                .one_or_none()
            if try_semeter is not None:
                continue
            semeters_to_add.append(db.Semeters(semeter['name']))
        return {
            'success': utils.db_insert(semeters_to_add)
        }

class Semeter(Resource):
    def get(self, semeter_name):
        try:
            jwt = utils.get_jwt()
            role = jwt['role']
        except Exception:
            return utils.return_auth_err()
        required_roles = ['manager', 'admin']
        if role not in required_roles:
            return utils.return_unauthorized()
        semeter = db.Semeters.query \
            .filter(db.Semeters.name == semeter_name) \
            .one_or_none()
        semeter_schema = db.SemetersSchema()
        return semeter_schema.dump(semeter)
    
    def post(self, semeter_name):
        try:
            jwt = utils.get_jwt()
            role = jwt['role']
        except Exception:
            return utils.return_auth_err()
        required_roles = ['manager', 'admin']
        if role not in required_roles:
            return utils.return_unauthorized()
        try_semeter = db.Semeters.query \
            .filter(db.Semeters.name == semeter_name) \
            .one_or_none()
        if try_semeter is not None:
            return {
                'success': False,
                'message': 'Phòng đã tồn tại'
            }
        room = db.Semeters(semeter_name)
        return {
            'success': utils.db_insert([room])
        }
    
    def delete(self, semeter_name):
        try:
            jwt = utils.get_jwt()
            role = jwt['role']
        except Exception:
            return utils.return_auth_err()
        required_roles = ['manager', 'admin']
        if role not in required_roles:
            return utils.return_unauthorized()
        room = db.Semeters.query \
            .filter(db.Semeters.name == semeter_name) \
            .first()
        if room is not None:
            return {
                'success': utils.db_delete([room])
            }
        return {
            'success': False,
            'message': 'Toà nhà không tồn tại'
        }
