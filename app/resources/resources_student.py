from flask import Flask, request, jsonify
from flask import json
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token, create_refresh_token
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from app.config import Config
from app.models.model import db, tbl_users, tbl_students
from app.utils.additional_handler import ResponseHandler

class GetAllStudentResource(Resource, ResponseHandler):
    @jwt_required()
    def get(self):
        current_user_identity = get_jwt_identity()
        current_user_role = current_user_identity['role']
        
        if current_user_role != 1:
            return self.error_response("Unauthorized access", 403)
        
        students = tbl_students.query.all()
   
        if not students:
            return self.error_response("No Student found", 404)
            
        students_data = [{
            "id":student.id,
            "nisn":student.nisn,
            "nama":student.nama,
            "alamat":student.alamat,
            "kelas":student.kelas,
            "attendance_id":student.attendance_id
        }for student in students]
            
        return self.success_response("Success",
                                        data=students_data,
                                    )
 

class PostStudentResource(Resource, ResponseHandler):
    @jwt_required()
    def post(self):
        current_user_identity = get_jwt_identity()
        current_user_role = current_user_identity['role']
        
        if current_user_role != 1:
            return self.error_response("Unauthorized access", 403)
        
        data = request.get_json()
        
        new_students = tbl_students(
            nisn=data.get('nisn'),
            nama=data.get('nama'),
            alamat=data.get('alamat'),
            kelas=data.get('kelas'),
            attendance_id=data.get('attendance_id')
        )
        
        db.session.add(new_students)
        db.session.commit()
        
        return self.success_response("student insert successfully")
    

class StudentResource(Resource, ResponseHandler):
    @jwt_required()
    def get(self, student_id):
        current_user_identity = get_jwt_identity()
        current_user_role = current_user_identity['role']
        
        if current_user_role != 1:
            return self.error_response("Unauthorized access", 403)
        
        if student_id is not None:
            student = tbl_students.query.get(student_id)
            
            if not student:
                return self.error_response("No Student found", 404)
        
            student_data = {
            "id":student.id,
            "nisn":student.nisn,
            "nama":student.nama,
            "alamat":student.alamat,
            "kelas":student.kelas,
            "attendance_id":student.attendance_id
            }
            
            return self.success_response("Success", 
                                            data=student_data,
                                            id=student.id,
                                            nisn=student.nisn,
                                            nama=student.nama,
                                            alamat=student.alamat,
                                            kelas=student.kelas,
                                            attendance_id=student.attendance_id                                        
                                        )
        
    @jwt_required()
    def put(self, student_id):
        current_user_identity = get_jwt_identity()
        current_user_role = current_user_identity['role']
        
        if current_user_role != 1:
            return self.error_response("Unauthorized access", 403)
        
        student = tbl_students.query.get(student_id)
        
        if not student:
            return self.error_response("No data Student found", 404)
        
        data = request.get_json()
        
        student.nisn = data.get('nisn')
        student.nama = data.get('nama')
        student.alamat = data.get('alamat')
        student.kelas = data.get('kelas')
        student.attendance_id = data.get('attendance_id')
        
        db.session.commit()
        
        return self.success_response("Student data has been Updated Successfully")
    
    @jwt_required()
    def patch(self,student_id):
        currrent_user_identity = get_jwt_identity()
        current_user_role = currrent_user_identity['role']
        
        if current_user_role != 1:
            return self.error_response("unauthorized access", 403)
        
        student = tbl_students.query.get(student_id)
        
        if not student:
            return self.error_response("no student found", 404)
        
        data = request.get_json()

        if 'nisn' in data:
            student.nisn = data['nisn']
        if 'nama' in data:
            student.nama = data['nama']
        if 'alamat' in data:
            student.alamat = data['alamat']
        if 'kelas' in data:
            student.kelas = data['kelas']
        if 'attendance_id' in data:
            student.attendance_id = data['attendance_id']
                
        db.session.commit()
        
        return self.success_response("Student data has been updated successfully")
   
    
    @jwt_required()
    def delete(self, student_id):
        current_user_identity = get_jwt_identity()
        current_user_role = current_user_identity['role']
        
        if current_user_role != 1:
            return self.error_response("Unauthorized access", 403)
        
        student = tbl_students.query.get(student_id)
        
        if not student:
            return self.error_response("No Student found with that id", 404)
                
        db.session.delete(student)
        db.session.commit()
        
        return self.success_response("student data has Delete Successfully")
    
class DeleteAllStudentResource(Resource, ResponseHandler):
    @jwt_required()
    def get(self):
        current_user_identity = get_jwt_identity()
        current_user_role = current_user_identity['role']
        
        if current_user_role != 1:
            return self.error_response("Unauthorized access", 403)
        
        students = tbl_students.query.all()
   
        if not students:
            return self.error_response("No Student found", 404)
        
        db.session.delete(students)
        db.session.commit()    
            
        return self.success_response("all students data has Delete Successfully")
