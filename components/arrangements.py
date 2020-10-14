import db
from flask import request
from flask_restful import Resource
import utils

class Arrangements(Resource):
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
        return semeter_schema.dump(semeter)['arrangements']
