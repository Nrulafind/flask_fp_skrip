from flask import Flask,request, jsonify
from flask import json
from flask_restful import Api 
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from app.models.model import db, tbl_users, tbl_students  # Import the db instance
from app.resources.resource_ import get, login, register, refresh
from app.resources.resources_attendance import AttendanceResource, PostAttendanceResource ,GetAllAttendanceResource, DeleteAllAttendanceResource
from app.resources.resources_class import ClassResource, GetAllClassResource, PostClassResource, DeleteAllClassResource
from app.resources.resources_parent import ParentResource,GetAllParentResource,PostParentResource,DeleteAllParentResource
from app.resources.resources_prediction import PostPredictions
from app.resources.resources_semester import SemesterResource, GetAllSemesterResource, PostSemesterResource, DeleteAllSemesterResource 
from app.resources.resources_student import StudentResource, PostStudentResource, GetAllStudentResource, DeleteAllStudentResource
from app.resources.resources_teacher import TeacherResource, GetAllTeacherResource, PostTeacherResource, DeleteAllTeacherResource

from app.config import Config
import os

app = Flask(__name__)
api = Api(app)
CORS(app)

# Use configuration from config.py
app.config.from_object(Config)

# Initialize SQLAlchemy, JWT, Bcrypt
db.init_app(app)  # Initialize the db instance with the app
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

# Add resources to the API
api.add_resource(get, '/api/')

api.add_resource(register, '/api/register')
api.add_resource(login, '/api/login')
api.add_resource(refresh, '/api/refresh')

api.add_resource(GetAllAttendanceResource, '/api/attendance')
api.add_resource(PostAttendanceResource, '/api/attendance')
api.add_resource(AttendanceResource, '/api/attendance/<attendance_id>/')
api.add_resource(DeleteAllAttendanceResource, '/api/attendance')

api.add_resource(GetAllClassResource, '/api/class')
api.add_resource(PostClassResource, '/api/class')
api.add_resource(ClassResource, '/api/class/<class_id>')
api.add_resource(DeleteAllClassResource, '/api/class')

api.add_resource(GetAllParentResource, '/api/parent')
api.add_resource(PostParentResource, '/api/parent')
api.add_resource(ParentResource, '/api/parent/<parent_id>')
api.add_resource(DeleteAllParentResource, '/api/parent')

api.add_resource(PostPredictions, '/api/prediction')

api.add_resource(GetAllSemesterResource, '/api/semester')
api.add_resource(PostSemesterResource, '/api/semester')
api.add_resource(SemesterResource, '/api/semester/<semester_id>')
api.add_resource(DeleteAllSemesterResource, '/api/semester')

api.add_resource(GetAllStudentResource, '/api/student')
api.add_resource(PostStudentResource, '/api/student')
api.add_resource(StudentResource, '/api/student/<student_id>')
api.add_resource(DeleteAllStudentResource, '/api/student')

api.add_resource(GetAllTeacherResource, '/api/teacher')
api.add_resource(PostTeacherResource, '/api/teacher')
api.add_resource(TeacherResource, '/api/teacher/<teacher_id>')
api.add_resource(DeleteAllTeacherResource, '/api/teacher')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8090)), debug=True)
