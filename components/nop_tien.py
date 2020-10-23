import db
from flask import request
from flask_restful import Resource
import utils

class NopTienList(Resource):
    def get(self):
        try:
            jwt = utils.get_jwt()
            role = jwt['role']
        except Exception:
            return utils.return_auth_err()
        required_roles = ['manager', 'admin']
        if role not in required_roles:
            return utils.return_unauthorized()
        nt = db.NopTien.query.all()
        nt_schema = db.NopTienSchema(many=True)
        return nt_schema.dump(nt)

class NopTien(Resource):
    def post(self, student_id):
        try:
            data = request.get_json()
            jwt = utils.get_jwt()
            role = jwt['role']
        except Exception:
            return utils.return_auth_err()
        required_roles = ['manager', 'admin']
        if role not in required_roles:
            return utils.return_unauthorized()
        nt = db.NopTien.query \
            .filter(db.NopTien.student_id == student_id) \
            .filter(db.NopTien.dot_id == data['dot_id']) \
            .first()
        if nt is not None:
            nt.trang_thai = 1
            return {
                'success': utils.db_insert([nt])
            }
        return {
            'success': False,
            'message': 'Không tồn tại'
        }
