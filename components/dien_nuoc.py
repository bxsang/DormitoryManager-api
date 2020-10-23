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

class TinhTienDN(Resource):
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
        arrangements = {}
        dien_nuoc_list = {}
        for dn in data:
            arrangement = db.RoomArrangements.query \
                .filter(db.RoomArrangements.room_name == dn['room_name']) \
                .filter(db.RoomArrangements.semeter_name == dn['semeter_name']) \
                .all()
            arrangement_schema = db.RoomArrangementsSchema(many=True).dump(arrangement)
            arrangements[dn['room_name']] = arrangement_schema
            dien_nuoc = db.DienNuoc.query \
                .filter(db.DienNuoc.dot_id == dn['dot_id']) \
                .filter(db.DienNuoc.room_name == dn['room_name']) \
                .one_or_none()
            dien_nuoc_list[dn['room_name']] = db.DienNuocSchema().dump(dien_nuoc)
        gia_dn = db.GiaDienNuocSchema().dump(db.GiaDienNuoc.query.one_or_none())
        nop_tien_list = []
        nop_tien_list2 = []
        for room in arrangements:
            for arrangement in arrangements[room]:
                if dien_nuoc_list[room]:
                    tong_tien = dien_nuoc_list[room]['water']*gia_dn['nuoc'] + dien_nuoc_list[room]['electricity']*gia_dn['dien']
                    nop_tien_list.append(db.NopTien(arrangement['student_id'], tong_tien, 0, dien_nuoc_list[room]['dot_id']))
                    nop_tien_list2.append([arrangement['student_id'], tong_tien, 0, dien_nuoc_list[room]['dot_id']])
        
        return {
            'success': utils.db_insert(nop_tien_list),
            'result': nop_tien_list2
        }
