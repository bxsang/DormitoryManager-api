import db
from flask import request
from flask_restful import Resource
import utils

class Violations(Resource):
    def get(self):
        try:
            jwt = utils.get_jwt()
            role = jwt['role']
        except Exception:
            return utils.return_auth_err()
        required_roles = ['manager', 'admin']
        if role not in required_roles:
            return utils.return_unauthorized()
        violations = db.Violations.query.all()
        violations_schema = db.ViolationsSchema(many=True)
        return violations_schema.dump(violations)
    
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
        violations_to_add = []
        for violation in data:
            violations_to_add.append(db.Violations(violation['student_id'], violation['semeter_name'], violation['employee_id'], violation['message']))
        return {
            'success': utils.db_insert(violations_to_add)
        }

class Violation(Resource):
    def delete(self, violation_id):
        try:
            jwt = utils.get_jwt()
            role = jwt['role']
        except Exception:
            return utils.return_auth_err()
        required_roles = ['manager', 'admin']
        if role not in required_roles:
            return utils.return_unauthorized()
        violation = db.Violations.query \
            .filter(db.Violations.id == violation_id) \
            .first()
        if violation is not None:
            return {
                'success': utils.db_delete([violation])
            }
        return {
            'success': False,
            'message': 'Lỗi không tồn tại'
        }
