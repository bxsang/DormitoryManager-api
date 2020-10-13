from config import app, api
from components.managers import Managers, Manager, ManagerLogin
from components.students import Students, Student, StudentLogin
from components.current_users import CurrentUser

api.add_resource(Managers, '/managers')
api.add_resource(Manager, '/managers/<manager_id>')
api.add_resource(ManagerLogin, '/managers/login')
api.add_resource(Students, '/students')
api.add_resource(Student, '/students/<student_id>')
api.add_resource(StudentLogin, '/students/login')
api.add_resource(CurrentUser, '/me')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
