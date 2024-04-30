from flask import Flask, request, jsonify
from flask import json
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token, create_refresh_token
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from app.config import Config
from app.models.model import db, tbl_users, tbl_classes
from app.utils.additional_handler import ResponseHandler

class GetAllClassResource(Resource, ResponseHandler):
    @jwt_required()
    def get(self):
        current_user_identity = get_jwt_identity()
        current_user_role = current_user_identity['role']
        
        if current_user_role != 1:
            return self.error_response("Unauthorized access", 403)
            
        kls_ = tbl_classes.query.all()
            
        if not kls_:
            return self.error_response("No Class found", 404)
            
        class_data_ = [{
            "id":kls.id,
            "nama_kelas":kls.nama_kelas,
            "wali_kelas":kls.wali_kelas,
        }for kls in kls_]
            
        return self.success_response("Success", 
                                    data=class_data_,
                                    # id=kls.id,
                                    # nama_kelas=kls.nama_kelas,
                                    # wali_kelas=kls.wali_kelas
                                    )

class PostClassResource(Resource, ResponseHandler):
    @jwt_required()
    def post(self):
        current_user_identity = get_jwt_identity()
        current_user_role = current_user_identity['role']
        
        if current_user_role != 1:
            return self.error_response("Unauthorized access", 403)
        
        data = request.get_json()
        
        new_kls = tbl_classes(
            nama_kelas=data.get('nama_kelas'),
            wali_kelas=data.get('wali_kelas')
        )
        
        db.session.add(new_kls)
        db.session.commit()
        
        return self.success_response("class insert successfully")


class ClassResource(Resource, ResponseHandler):
    def get(self, class_id=None):
        current_user_identity = get_jwt_identity()
        current_user_role = current_user_identity['role']
        
        if current_user_role != 1:
            return self.error_response("Unauthorized access", 403)
        
        if class_id is not None:
            kls = tbl_classes.query.get(class_id)
            
            if not kls:
                return self.error_response("No Class found", 404)
        
            class_data = {
            "id":kls.id,
            "nama_kelas":kls.nama_kelas,
            "wali_kelas":kls.wali_kelas,
            }
            
            return self.success_response("Success", data=class_data)
        
    
    @jwt_required()
    def put(self, class_id):
        current_user_identity = get_jwt_identity()
        current_user_role = current_user_identity['role']
        
        if current_user_role != 1:
            return self.error_response("Unauthorized access", 403)
        
        kls = tbl_classes.query.get(class_id)
        
        if not kls:
            return self.error_response("No such class found", 404)
        
        data = request.get_json()
        
        kls.nama_kelas = data.get('nama_kelas')
        kls.wali_kelas = data.get('wali_kelas')
        
        db.session.commit()
        
        return self.success_response("Class Update Successfully")
    
    @jwt_required()
    def patch(self,class_id):
        currrent_user_identity = get_jwt_identity()
        current_user_role = current_user_identity['role']
        
        if current_user_role != 1:
            return self.error_response("unauthorized access", 403)
        
        kls = tbl_classes.query.get(class_id)
        
        if not kls:
            return self.error_response("no kls found", 404)
        
        data = request.get_json()

        if 'nama_kelas' in data:
            kls.nama_kelas = data['nama_kelas']
        if 'wali_kelas' in data:
            kls.wali_kelas = data['wali_kelas']
            
        db.session.commit()
        
        return self.success_response("Class data has been updated successfully")
    
    
    @jwt_required()
    def delete(self, class_id):
        current_user_identity = get_jwt_identity()
        current_user_role = current_user_identity['role']
        
        if current_user_role != 1:
            return self.error_response("Unauthorized access", 403)
        
        kls = tbl_classes.query.get(class_id)
        
        if not kls:
            return self.error_response("No such class found", 404)
                
        db.session.delete(kls)
        db.session.commit()
        
        return self.success_response("Class Delete Successfully")
    
class DeleteAllClassResource(Resource, ResponseHandler):
    @jwt_required()
    def get(self):
        current_user_identity = get_jwt_identity()
        current_user_role = current_user_identity['role']
        
        if current_user_role != 1:
            return self.error_response("Unauthorized access", 403)
        
        classes = tbl_classes.query.all()
   
        if not students:
            return self.error_response("No Class found", 404)
        
        db.session.delete(classes)
        db.session.commit()    
            
        return self.success_response("all class data has Delete Successfully")

    