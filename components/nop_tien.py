import db
from flask import request
from flask_restful import Resource
import utils

class NopTien(Resource):
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
        data_to_add = []
        for d in data:
            nt = db.NopTien.query \
                .filter(db.NopTien.student_id == d['student_id']) \
                .filter(db.NopTien.dot_id == d['dot_id']) \
                .first()
            if nt is not None:
                nt.trang_thai = 1
                data_to_add.append(nt)
        try:
            for nt in data_to_add:
                nt.trang_thai = 1
                utils.db_insert([nt])
            return {
                'success': True
            }
        except Exception:
            return {
                'success': False
            }

class NopTien2(Resource):
    def delete(self, id):
        try:
            jwt = utils.get_jwt()
            role = jwt['role']
        except Exception:
            return utils.return_auth_err()
        required_roles = ['manager', 'admin']
        if role not in required_roles:
            return utils.return_unauthorized()
        nt = db.NopTien.query \
            .filter(db.NopTien.id == id) \
            .first()
        if nt is not None:
            return {
                'success': utils.db_delete([nt])
            }
        return {
            'success': False,
            'message': 'Không tồn tại'
        }
