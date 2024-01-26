from flask import Flask, request, jsonify
from flask import json
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token, create_refresh_token
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from app.config import Config
from app.models.model import db, tbl_users, tbl_teachers
from app.utils.additional_handler import ResponseHandler

class GetAllTeacherResource(Resource, ResponseHandler):
    @jwt_required()
    def get(self):
        current_user_identity = get_jwt_identity()
        current_user_role = current_user_identity['role']
        
        if current_user_role != 1:
            return self.error_response("Unauthorized access", 403)
            
        teachers = tbl_teachers.query.all()
            
        if not teachers:
            return self.error_response("No Teacher found", 404)
            
            teachers_data = [{
                "id":teacher.id,
                "nik":teacher.nik,
                "nama":teacher.nama,
                "alamat":teacher.alamat,
                "status":teacher.status
            }for teacher in teachers]
            
            return self.success_response("Success", teachers_data=teachers_data)
 

class PostTeacherResource(Resource, ResponseHandler):
    @jwt_required()
    def post(self):
        current_user_identity = get_jwt_identity()
        current_user_role = current_user_identity['role']
        
        if current_user_role != 1:
            return self.error_response("Unauthorized access", 403)
        
        data = request.get_json()
        
        new_teachers = tbl_teachers(
            nik=data.get('nik'),
            nama=data.get('nama'),
            alamat=data.get('alamat'),
            status=data.get('status')
        )
        
        db.session.add(new_teachers)
        db.session.commit()
        
        return self.success_response("teacher insert successfully")
    

class TeacherResource(Resource, ResponseHandler):
    @jwt_required()
    def get(self, teacher_id):
        current_user_identity = get_jwt_identity()
        current_user_role = current_user_identity['role']
        
        if current_user_role != 1:
            return self.error_response("Unauthorized access", 403)
        
        if teacher_id is not None:
            teacher = tbl_teachers.query.get(teacher_id)
            
            if not teacher:
                return self.error_response("No Teacher found", 404)
        
            teacher_data = {
            "id":teacher.id,
            "nik":teacher.nik,
            "nama":teacher.nama,
            "alamat":teacher.alamat,
            "status":teacher.status
            }
            
            return self.success_response("Success", teacher_data=teacher_data)
    
    @jwt_required()
    def put(self, teacher_id):
        current_user_identity = get_jwt_identity()
        current_user_role = current_user_identity['role']
        
        if current_user_role != 1:
            return self.error_response("Unauthorized access", 403)
        
        teacher = tbl_teachers.query.get(teacher_id)
        
        if not teacher:
            return self.error_response("No data Teacher found", 404)
        
        data = request.get_json()
        
        teacher.nik = data.get('nik')
        teacher.nama = data.get('nama')
        teacher.alamat = data.get('alamat')
        teacher.status = data.get('status')
        
        db.session.commit()
        
        return self.success_response("Teacher data has been Updated Successfully")
    
    @jwt_required()
    def patch(self,teacher_id):
        currrent_user_identity = get_jwt_identity()
        current_user_role = current_user_identity['role']
        
        if current_user_role != 1:
            return self.error_response("unauthorized access", 403)
        
        teacher = tbl_teachers.query.get(teacher_id)
        
        if not teacher:
            return self.error_response("no teacher found", 404)
        
        data = request.get_json()
        
        if 'nik' in data:
            teacher.nik = data['nik']
        if 'nama' in data:
            teacher.nama = data['nama']
        if 'alamat' in data:
            teacher.alamat = data['alamat']
        if 'status' in data:
            teacher.status = data['status']
            
        db.session.commit()
        
        return self.success_response("Teacher data has been updated successfully")
    
    @jwt_required()
    def delete(self, teacher_id):
        current_user_identity = get_jwt_identity()
        current_user_role = current_user_identity['role']
        
        if current_user_role != 1:
            return self.error_response("Unauthorized access", 403)
        
        teacher = tbl_teachers.query.get(teacher_id)
        
        if not teacher:
            return self.error_response("No Teacher found with that id", 404)
                
        db.session.delete(teacher)
        db.session.commit()
        
        return self.success_response("teacher data has Delete Successfully")
    
class DeleteAllTeacherResource(Resource, ResponseHandler):
    @jwt_required()
    def get(self):
        current_user_identity = get_jwt_identity()
        current_user_role = current_user_identity['role']
        
        if current_user_role != 1:
            return self.error_response("Unauthorized access", 403)
        
        teachers = tbl_teachers.query.all()
   
        if not teachers:
            return self.error_response("No Data teachers found", 404)
        
        db.session.delete(teachers)
        db.session.commit()    
            
        return self.success_response("all teachers data has Delete Successfully")

    