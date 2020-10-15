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

    def post(self, semeter_name):
        try:
            data = request.get_json()
            jwt = utils.get_jwt()
            role = jwt['role']
        except Exception:
            return utils.return_auth_err()
        required_roles = ['manager', 'admin']
        if role not in required_roles:
            return utils.return_unauthorized()
        # {"students":["student_id",...], "building":["building_name",...]}
        data_students = data['students']
        data_building = data['building']

        rooms = []
        for building_name in data_building:
            building = db.Building.query \
                .filter(db.Building.name == building_name) \
                .one_or_none()
            building_schema = db.BuildingSchema()
            for room in building_schema.dump(building)['rooms']:
                rooms.append(room)
            if not rooms:
                return {
                    'success': False,
                    'message': 'Rooms not found'
                }

        ok = []
        result = []
        result2 = []
        for room in rooms:
            slot_count = db.RoomArrangements.query \
                .filter(db.RoomArrangements.room_name == room['name']) \
                .filter(db.RoomArrangements.semeter_name == semeter_name) \
                .count()
            if slot_count < room['capacity']:
                slot_left = room['capacity'] - slot_count - 1
                for student_id in data_students:
                    if student_id in ok:
                        continue
                    if slot_left < 0:
                        break
                    result.append(db.RoomArrangements(semeter_name, student_id, room['name'], jwt['id']))
                    result2.append({'student_id': student_id, 'room': room['name'], 'slot_left': slot_left})
                    ok.append(student_id)
                    slot_left -= 1
        
        return {
            'success': utils.db_insert(result),
            'result': result2
        }
