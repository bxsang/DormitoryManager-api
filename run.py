from config import app, api
from components.managers import Managers, Manager, ManagerLogin
from components.students import Students, Student, StudentLogin, StudentArrangements
from components.current_users import CurrentUser
from components.building import Buildings, Building, BuildingRooms
from components.rooms import Rooms, Room, RoomArrangements, RoomArrangementsBySemeter
from components.semeters import Semeters, Semeter
from components.arrangements import Arrangements
from components.attendance import Attendance
from components.violations import Violations, Violation
from components.dot_thu import DotThu, DotThu2
from components.dien_nuoc import DienNuoc, DienNuoc2, TinhTienDN

api.add_resource(Managers, '/managers')
api.add_resource(Manager, '/managers/<manager_id>')
api.add_resource(ManagerLogin, '/managers/login')
api.add_resource(Students, '/students')
api.add_resource(Student, '/students/<student_id>')
api.add_resource(StudentArrangements, '/students/<student_id>/arrangements')
api.add_resource(StudentLogin, '/students/login')
api.add_resource(CurrentUser, '/me')
api.add_resource(Buildings, '/buildings')
api.add_resource(Building, '/buildings/<building_name>')
api.add_resource(BuildingRooms, '/buildings/<building_name>/rooms')
api.add_resource(Rooms, '/rooms')
api.add_resource(Room, '/rooms/<room_name>')
api.add_resource(RoomArrangements, '/rooms/<room_name>/arrangements')
api.add_resource(RoomArrangementsBySemeter, '/rooms/<room_name>/arrangements/<semeter_name>')
api.add_resource(Semeters, '/semeters')
api.add_resource(Semeter, '/semeters/<semeter_name>')
api.add_resource(Arrangements, '/semeters/<semeter_name>/arrangements')
api.add_resource(Attendance, '/attendance/<date>')
api.add_resource(Violations, '/violations')
api.add_resource(Violation, '/violations/<violation_id>')
api.add_resource(DotThu, '/dot_thu')
api.add_resource(DotThu2, '/dot_thu/<dot_id>')
api.add_resource(DienNuoc, '/dien_nuoc')
api.add_resource(DienNuoc2, '/dien_nuoc/<dn_id>')
api.add_resource(TinhTienDN, '/dien_nuoc/tinh_tien')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
