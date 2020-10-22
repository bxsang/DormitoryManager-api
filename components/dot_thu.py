import db
from flask import request
from flask_restful import Resource
import utils
from datetime import date

class DotThu(Resource):
    def get(self):
        try:
            jwt = utils.get_jwt()
            role = jwt['role']
        except Exception:
            return utils.return_auth_err()
        required_roles = ['manager', 'admin']
        if role not in required_roles:
            return utils.return_unauthorized()
        dot = db.DotThuTien.query.all()
        dot_schema = db.DotThuTienSchema(many=True)
        return dot_schema.dump(dot)
    
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
        dot_to_add = []
        today = date.today()
        for dot in data:
            dot_to_add.append(db.DotThuTien(None, dot['name'], str(today.strftime("%Y-%m-%d")), dot['semeter_name']))
        return {
            'success': utils.db_insert(dot_to_add)
        }

class DotThu2(Resource):
    def delete(self, dot_id):
        try:
            jwt = utils.get_jwt()
            role = jwt['role']
        except Exception:
            return utils.return_auth_err()
        required_roles = ['manager', 'admin']
        if role not in required_roles:
            return utils.return_unauthorized()
        dot = db.DotThuTien.query \
            .filter(db.DotThuTien.id == dot_id) \
            .first()
        if dot is not None:
            return {
                'success': utils.db_delete([dot])
            }
        return {
            'success': False,
            'message': 'Đợt thu tiền không tồn tại'
        }
