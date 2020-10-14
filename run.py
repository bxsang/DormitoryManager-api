from config import app, api
from components.managers import Managers, Manager, ManagerLogin
from components.students import Students, Student, StudentLogin
from components.current_users import CurrentUser
from components.building import Buildings, Building
from components.rooms import Rooms, Room
from components.semeters import Semeters, Semeter
from components.arrangements import Arrangements

api.add_resource(Managers, '/managers')
api.add_resource(Manager, '/managers/<manager_id>')
api.add_resource(ManagerLogin, '/managers/login')
api.add_resource(Students, '/students')
api.add_resource(Student, '/students/<student_id>')
api.add_resource(StudentLogin, '/students/login')
api.add_resource(CurrentUser, '/me')
api.add_resource(Buildings, '/buildings')
api.add_resource(Building, '/buildings/<building_name>')
api.add_resource(Rooms, '/rooms')
api.add_resource(Room, '/rooms/<room_name>')
api.add_resource(Semeters, '/semeters')
api.add_resource(Semeter, '/semeters/<semeter_name>')
api.add_resource(Arrangements, '/semeters/<semeter_name>/arrangements')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
