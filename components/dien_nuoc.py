import db
from flask import request
from flask_restful import Resource
import utils
from datetime import date

class DienNuoc(Resource):
    def get(self):
        try:
            jwt = utils.get_jwt()
            role = jwt['role']
        except Exception:
            return utils.return_auth_err()
        required_roles = ['manager', 'admin']
        if role not in required_roles:
            return utils.return_unauthorized()
        dn = db.DienNuoc.query.all()
        dn_schema = db.DienNuocSchema(many=True)
        return dn_schema.dump(dn)

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
        dn_to_add = []
        today = date.today()
        for dn in data:
            dn_to_add.append(db.DienNuoc(None, dn['room_name'], str(today.strftime("%Y-%m-%d")), dn['semeter_name'], dn['water'], dn['electricity'], dn['dot_id']))
        return {
            'success': utils.db_insert(dn_to_add)
        }

class DienNuoc2(Resource):
    def delete(self, dn_id):
        try:
            jwt = utils.get_jwt()
            role = jwt['role']
        except Exception:
            return utils.return_auth_err()
        required_roles = ['manager', 'admin']
        if role not in required_roles:
            return utils.return_unauthorized()
        dn = db.DienNuoc.query \
            .filter(db.DienNuoc.id == dn_id) \
            .first()
        if dn is not None:
            return {
                'success': utils.db_delete([dn])
            }
        return {
            'success': False,
            'message': 'Không tồn tại'
        }
