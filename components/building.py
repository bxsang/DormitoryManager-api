import db
from flask import request
from flask_restful import Resource
import utils

class Buildings(Resource):
    def get(self):
        try:
            jwt = utils.get_jwt()
            role = jwt['role']
        except Exception:
            return utils.return_auth_err()
        required_roles = ['manager', 'admin']
        if role not in required_roles:
            return utils.return_unauthorized()
        building = db.Building.query.all()
        building_schema = db.BuildingSchema(many=True)
        return building_schema.dump(building)
    
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
        building_to_add = []
        for building in data:
            try_building = db.Building.query \
                .filter(db.Building.name == building['name']) \
                .one_or_none()
            if try_building is not None:
                continue
            building_to_add.append(db.Building(building['name']))
        return {
            'success': utils.db_insert(building_to_add)
        }

class Building(Resource):
    def get(self, building_name):
        try:
            jwt = utils.get_jwt()
            role = jwt['role']
        except Exception:
            return utils.return_auth_err()
        required_roles = ['manager', 'admin']
        if role not in required_roles:
            return utils.return_unauthorized()
        building = db.Building.query \
            .filter(db.Building.name == building_name) \
            .one_or_none()
        building_schema = db.BuildingSchema()
        return building_schema.dump(building)

    def post(self, building_name):
        try:
            jwt = utils.get_jwt()
            role = jwt['role']
        except Exception:
            return utils.return_auth_err()
        required_roles = ['manager', 'admin']
        if role not in required_roles:
            return utils.return_unauthorized()
        try_building = db.Building.query \
            .filter(db.Building.name == building_name) \
            .one_or_none()
        if try_building is not None:
            return {
                'success': False,
                'message': 'Toà nhà đã tồn tại'
            }
        building = db.Building(building_name)
        return {
            'success': utils.db_insert([building])
        }
    
    def delete(self, building_name):
        try:
            jwt = utils.get_jwt()
            role = jwt['role']
        except Exception:
            return utils.return_auth_err()
        required_roles = ['manager', 'admin']
        if role not in required_roles:
            return utils.return_unauthorized()
        building = db.Building.query \
            .filter(db.Building.name == building_name) \
            .first()
        if building is not None:
            return {
                'success': utils.db_delete([building])
            }
        return {
            'success': False,
            'message': 'Toà nhà không tồn tại'
        }
