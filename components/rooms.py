import db
from flask import request
from flask_restful import Resource
import utils

class Rooms(Resource):
    def get(self):
        try:
            jwt = utils.get_jwt()
            role = jwt['role']
        except Exception:
            return utils.return_auth_err()
        required_roles = ['manager', 'admin']
        if role not in required_roles:
            return utils.return_unauthorized()
        rooms = db.Rooms.query.all()
        rooms_schema = db.RoomsSchema(many=True)
        return rooms_schema.dump(rooms)
    
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
        rooms_to_add = []
        for rooms in data:
            try_rooms = db.Rooms.query \
                .filter(db.Rooms.name == rooms['name']) \
                .one_or_none()
            if try_rooms is not None:
                continue
            rooms_to_add.append(db.Rooms(rooms['name'], rooms['capacity'], rooms['building_name']))
        return {
            'success': utils.db_insert(rooms_to_add)
        }

class Room(Resource):
    def get(self, room_name):
        try:
            jwt = utils.get_jwt()
            role = jwt['role']
        except Exception:
            return utils.return_auth_err()
        required_roles = ['manager', 'admin']
        if role not in required_roles:
            return utils.return_unauthorized()
        room = db.Rooms.query \
            .filter(db.Rooms.name == room_name) \
            .one_or_none()
        room_schema = db.RoomsSchema()
        return room_schema.dump(room)
    
    def post(self, room_name):
        try:
            data = request.get_json()
            jwt = utils.get_jwt()
            role = jwt['role']
        except Exception:
            return utils.return_auth_err()
        required_roles = ['manager', 'admin']
        if role not in required_roles:
            return utils.return_unauthorized()
        try_room = db.Rooms.query \
            .filter(db.Rooms.name == room_name) \
            .one_or_none()
        if try_room is not None:
            return {
                'success': False,
                'message': 'Phòng đã tồn tại'
            }
        room = db.Rooms(room_name, data['capacity'], data['building_name'])
        return {
            'success': utils.db_insert([room])
        }
    
    def delete(self, room_name):
        try:
            jwt = utils.get_jwt()
            role = jwt['role']
        except Exception:
            return utils.return_auth_err()
        required_roles = ['manager', 'admin']
        if role not in required_roles:
            return utils.return_unauthorized()
        room = db.Rooms.query \
            .filter(db.Rooms.name == room_name) \
            .first()
        if room is not None:
            return {
                'success': utils.db_delete([room])
            }
        return {
            'success': False,
            'message': 'Toà nhà không tồn tại'
        }
