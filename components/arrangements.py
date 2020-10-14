import db
from flask import request
from flask_restful import Resource
import utils

class Arrangements(Resource):
    def get(self):
        try:
            jwt = utils.get_jwt()
            role = jwt['role']
        except Exception:
            return utils.return_auth_err()
        required_roles = ['manager', 'admin']
        if role not in required_roles:
            return utils.return_unauthorized()
        arrangements = db.RoomArrangements.query.all()
        arrangements_schema = db.RoomArrangementsSchema(many=True)
        return arrangements_schema.dump(arrangements)
