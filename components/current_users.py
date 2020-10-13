import db
from flask_restful import Resource
from utils import get_jwt, return_auth_err

class CurrentUser(Resource):
    def get(self):
        try:
            jwt = get_jwt()
            role = jwt['role']
            person_id = jwt['id']
        except Exception:
            return return_auth_err()
        if role in ['manager', 'admin']:
            manager = db.Manager.query \
                .filter(db.Manager.id == person_id) \
                .one_or_none()
            manager_schema = db.ManagerSchema()
            return manager_schema.dump(manager)
        elif role == 'student':
            student = db.Student.query \
                .filter(db.Student.id == person_id) \
                .one_or_none()
            student_schema = db.StudentSchema()
            return student_schema.dump(student)
        return None
