from config import app, api
from components.users import ManagerList, Manager, ManagerLogin, StudentList, Student, StudentLogin, CurrentUser

api.add_resource(ManagerList, '/managers')
api.add_resource(Manager, '/managers/<manager_id>')
api.add_resource(ManagerLogin, '/managers/login')
api.add_resource(StudentList, '/students')
api.add_resource(Student, '/students/<student_id>')
api.add_resource(StudentLogin, '/students/login')
api.add_resource(CurrentUser, '/me')

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
