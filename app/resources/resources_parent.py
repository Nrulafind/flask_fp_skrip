from flask import Flask, request, jsonify
from flask import json
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token, create_refresh_token
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from app.config import Config
from app.models.model import db, tbl_users, tbl_parents
from app.utils.additional_handler import ResponseHandler

class GetAllParentResource(Resource, ResponseHandler):
    @jwt_required()
    def get(self):
        current_user_identity = get_jwt_identity()
        current_user_role = current_user_identity['role']
        
        if current_user_role != 1:
            return self.error_response("Unauthorized access", 403)
        
        parents = tbl_parents.query.all()
            
        if not parents:
            return self.error_response("No Parent found", 404)
            
        parents_data = [{
            "id":parent.id,
            "nama":parent.nama,
            "alamat":parent.alamat,
            "student_id":parent.student_id
        }for parent in parents]
            
        return self.success_response("Success",
                                        parents_data=parents_data,
                                        id=parent.id,
                                        nama=parent.nama,
                                        alamat=parent.alamat,
                                        student_id=parent.student_id          
                                    )
 

class PostParentResource(Resource, ResponseHandler):
    @jwt_required()
    def post(self):
        current_user_identity = get_jwt_identity()
        current_user_role = current_user_identity['role']
        
        if current_user_role != 1:
            return self.error_response("Unauthorized access", 403)
        
        data = request.get_json()
        
        new_parents = tbl_parents(
            nama=data.get('nama'),
            alamat=data.get('alamat'),
            student_id=data.get('student_id')
        )
        
        db.session.add(new_parents)
        db.session.commit()
        
        return self.success_response("parent insert successfully")
  


class ParentResource(Resource, ResponseHandler):
    @jwt_required()
    def get(self, parent_id):
        current_user_identity = get_jwt_identity()
        current_user_role = current_user_identity['role']
        
        if current_user_role != 1:
            return self.error_response("Unauthorized access", 403)
        
        if parent_id is not None:
            parent = tbl_parents.query.get(parent_id)
            
            if not parent:
                return self.error_response("No Parent found", 404)
        
            parent_data = {
            "id":parent.id,
            "nama":parent.nama,
            "alamat":parent.alamat,
            "student_id":parent.student_id
            }
            
            return self.success_response("Success", parent_data=parent_data)
        
    @jwt_required()
    def put(self, parent_id):
        current_user_identity = get_jwt_identity()
        current_user_role = current_user_identity['role']
        
        if current_user_role != 1:
            return self.error_response("Unauthorized access", 403)
        
        parent = tbl_parents.query.get(parent_id)
        
        if not parent:
            return self.error_response("No data Parent found", 404)
        
        data = request.get_json()
        
        parent.nama = data.get('nama')
        parent.alamat = data.get('alamat')
        parent.student_id = data.get('student_id')
        
        db.session.commit()
        
        return self.success_response("Parent data has been Updated Successfully")
    
    @jwt_required()
    def patch(self,parent_id):
        currrent_user_identity = get_jwt_identity()
        current_user_role = current_user_identity['role']
        
        if current_user_role != 1:
            return self.error_response("unauthorized access", 403)
        
        parent = tbl_parents.query.get(parent_id)
        
        if not parent:
            return self.error_response("no parent found", 404)
        
        data = request.get_json()

        if 'nama' in data:
            parent.nama = data['nama']
        if 'alamat' in data:
            parent.alamat = data['alamat']
        if 'student_id' in data:
            parent.student_id = data['student_id']
            
        db.session.commit()
        
        return self.success_response("Parent data has been updated successfully")
   
    
    @jwt_required()
    def delete(self, parent_id):
        current_user_identity = get_jwt_identity()
        current_user_role = current_user_identity['role']
        
        if current_user_role != 1:
            return self.error_response("Unauthorized access", 403)
        
        parent = tbl_parents.query.get(parent_id)
        
        if not parent:
            return self.error_response("No Parent found with that id", 404)
                
        db.session.delete(parent)
        db.session.commit()
        
        return self.success_response("parent data has Delete Successfully")
    
class DeleteAllParentResource(Resource, ResponseHandler):
    @jwt_required()
    def get(self):
        current_user_identity = get_jwt_identity()
        current_user_role = current_user_identity['role']
        
        if current_user_role != 1:
            return self.error_response("Unauthorized access", 403)
        
        parents = tbl_parents.query.all()
   
        if not parents:
            return self.error_response("No Data parents found", 404)
        
        db.session.delete(parents)
        db.session.commit()    
            
        return self.success_response("all parents data has Delete Successfully")
