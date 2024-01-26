from flask import Flask, request, jsonify
from flask import json
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token, create_refresh_token
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from app.config import Config
from app.models.model import db, tbl_users, tbl_semesters
from app.utils.additional_handler import ResponseHandler

class GetAllSemesterResource(Resource, ResponseHandler):
    @jwt_required()
    def get(self):
        current_user_identity = get_jwt_identity()
        current_user_role = current_user_identity['role']
        
        if current_user_role != 1:
            return self.error_response("Unauthorized access", 403)
            
        semesters = tbl_semesters.query.all()
            
        if not semesters:
            return self.error_response("No semesters found", 404)
            
        semesters_data = [{
            "id":semester.id,
            "nama_semester":semester.nama_semester,
            "grade":semester.grade,
            "prediction":semester.prediction,
            "date":semester.date,
            "student_id":semester.student_id,
            "teacher_id":semester.teacher_id
        }for semester in semesters]
            
        return self.success_response("Success", 
                                    semesters_data=semesters_data,
                                    id=semester.id,
                                    nama_semester=semester.nama_semester,
                                    grade=semester.grade,
                                    prediction=semester.prediction,
                                    date=semester.date,
                                    student_id=semester.student_id,
                                    teacher_id=semester.teacher_id
                                     )
 

class PostSemesterResource(Resource, ResponseHandler):
    @jwt_required()
    def post(self):
        current_user_identity = get_jwt_identity()
        current_user_role = current_user_identity['role']
        
        if current_user_role != 1:
            return self.error_response("Unauthorized access", 403)
        
        data = request.get_json()
        
        new_semesters = tbl_semesters(
            nama_semester=data.get('nama_semester'),
            grade=data.get('grade'),
            prediction=data.get('prediction'),
            date=data.get('date'),
            student_id=data.get('student_id'),
            teacher_id=data.get('teacher_id')
        )
        
        db.session.add(new_semesters)
        db.session.commit()
        
        return self.success_response("semester insert successfully")
    


class SemesterResource(Resource, ResponseHandler):
    @jwt_required()
    def get(self, semester_id):
        current_user_identity = get_jwt_identity()
        current_user_role = current_user_identity['role']
        
        if current_user_role != 1:
            return self.error_response("Unauthorized access", 403)
        
        if semester_id is not None:
            semester = tbl_semesters.query.get(semester_id)
            
            if not semester:
                return self.error_response("No Semester found", 404)
        
            semester_data = {
            "id":semester.id,
            "nama_semester":semester.nama_semester,
            "grade":semester.grade,
            "prediction":semester.prediction,
            "date":semester.date,
            "student_id":semester.student_id,
            "teacher_id":semester.teacher_id
            }
            
            return self.success_response("Success", semester_data=semester_data)
    
    @jwt_required()
    def put(self, semester_id):
        current_user_identity = get_jwt_identity()
        current_user_role = current_user_identity['role']
        
        if current_user_role != 1:
            return self.error_response("Unauthorized access", 403)
        
        semester = tbl_semesters.query.get(semester_id)
        
        if not semester:
            return self.error_response("No data Semester found", 404)
        
        data = request.get_json()
        
        semester.nama_semester = data.get('nama_semester')
        semester.grade = data.get('grade')
        semester.prediction = data.get('prediction')
        semester.date = data.get('date')
        semester.student_id = data.get('student_id')
        semester.teacher_id = data.get('teacher_id')
        
        db.session.commit()
        
        return self.success_response("Semester data has been Updated Successfully")
    
    @jwt_required()
    def patch(self,semester_id):
        currrent_user_identity = get_jwt_identity()
        current_user_role = current_user_identity['role']
        
        if current_user_role != 1:
            return self.error_response("unauthorized access", 403)
        
        semester = tbl_semesters.query.get(semester_id)
        
        if not semester:
            return self.error_response("no semester found", 404)
        
        data = request.get_json()

        if 'nama_semester' in data:
            semester.nama_semester = data['nama_semester']
        if 'grade' in data:
            semester.grade = data['grade']
        if 'prediction' in data:
            semester.prediction = data['prediction']
        if 'date' in data:
            semester.date = data['date']
        if 'student_id' in data:
            semester.student_id = data['student_id']
        if 'teacher_id' in data:
            semester.teacher_id = data['teacher_id']
                
        db.session.commit()
        
        return self.success_response("Semester data has been updated successfully")
   
    
    @jwt_required()
    def delete(self, semester_id):
        current_user_identity = get_jwt_identity()
        current_user_role = current_user_identity['role']
        
        if current_user_role != 1:
            return self.error_response("Unauthorized access", 403)
        
        semester = tbl_semesters.query.get(semester_id)
        
        if not semester:
            return self.error_response("No Semester found with that id", 404)
                
        db.session.delete(semester)
        db.session.commit()
        
        return self.success_response("semester data has Delete Successfully")

class DeleteAllSemesterResource(Resource, ResponseHandler):
    @jwt_required()
    def get(self):
        current_user_identity = get_jwt_identity()
        current_user_role = current_user_identity['role']
        
        if current_user_role != 1:
            return self.error_response("Unauthorized access", 403)
        
        semesters = tbl_semesters.query.all()
   
        if not semesters:
            return self.error_response("No Data semesters found", 404)
        
        db.session.delete(semesters)
        db.session.commit()    
            
        return self.success_response("all semesters data has Delete Successfully")
