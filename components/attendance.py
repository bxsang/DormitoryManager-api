import db
from flask import request
from flask_restful import Resource
import utils

class Attendance(Resource):
    def get(self, date):
        try:
            jwt = utils.get_jwt()
            role = jwt['role']
        except Exception:
            return utils.return_auth_err()
        required_roles = ['manager', 'admin']
        if role not in required_roles:
            return utils.return_unauthorized()
        attendance = db.Attendance.query \
            .filter(db.Attendance.date == date) \
            .all()
        attendance_schema = db.AttendanceSchema(many=True)
        return attendance_schema.dump(attendance)
    
    def post(self, date):
        try:
            data = request.get_json()
            jwt = utils.get_jwt()
            role = jwt['role']
        except Exception:
            return utils.return_auth_err()
        required_roles = ['manager', 'admin']
        if role not in required_roles:
            return utils.return_unauthorized()
        attendance_to_add = []
        for attendance in data:
            try_attendance = db.Attendance.query \
                .filter(db.Attendance.student_id == attendance['student_id']) \
                .filter(db.Attendance.date == date) \
                .one_or_none()
            if try_attendance is not None:
                continue
            attendance_to_add.append(db.Attendance(date, attendance['status'], attendance['student_id']))
        return {
            'success': utils.db_insert(attendance_to_add)
        }
