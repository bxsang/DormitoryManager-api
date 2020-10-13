import db
from flask_restful import Resource
from utils import get_jwt, return_auth_err, return_unauthorized

class EditStudent(Resource):
    def post(self, student_id):
        try:
            jwt = get_jwt()
            role = jwt['role']
        except Exception:
            return return_auth_err()
        required_roles = ['manager', 'admin']
        if role not in required_roles:
            return return_unauthorized()
