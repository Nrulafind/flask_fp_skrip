from flask import Flask, request, jsonify
from flask import json
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token, create_refresh_token
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from app.config import Config
from app.models.model import db, tbl_users
from app.utils.additional_handler import ResponseHandler

class GetAlluserResource(Resource, ResponseHandler):
    @jwt_required()
    def get(self):
        current_user_identity = get_jwt_identity()
        current_user_role = current_user_identity['role']
        
        if current_user_role != 1:
            return self.error_response("Unauthorized access", 403)
            
        users = tbl_users.query.all()
        
        if not users:
            return self.error_response("No user found", 404)
     
        users_data = [{
            "id":user.id,
            "email":user.email,
            "user_name":user.user_name,
            "password":user.password,
            "role":user.role,
            "status":user.status
        }for user in users]
            
        return self.success_response("Success", 
                                        data=users_data
                                    )       


class PostuserResource(Resource, ResponseHandler):
    @jwt_required()
    def post(self):
        current_user_identity = get_jwt_identity()
        current_user_role = current_user_identity['role']
        
        if current_user_role != 1:
            return self.error_response("Unauthorized access", 403)
        
        data = request.get_json()
        
        new_users = tbl_users(
            email=data.get('email'),
            user_name=data.get('user_name'),
            password=data.get('password'),
            role=data.get('role'),
            status=data.get('status')
        )
        
        db.session.add(new_users)
        db.session.commit()
        
        return self.success_response("user insert successfully")
    

class userResource(Resource, ResponseHandler):
    @jwt_required()
    def get(self, user_id):
        current_user_identity = get_jwt_identity()
        current_user_role = current_user_identity['role']
        
        if current_user_role != 1:
            return self.error_response("Unauthorized access", 403)
        
        if user_id is not None:
            user = tbl_users.query.get(user_id)
            
            if not user:
                return self.error_response("No user found", 404)
        
            user_data = {
            "id":user.id,
            "email":user.email,
            "user_name":user.user_name,
            "password":user.password,
            "role":user.role,
            "status":user.status
            }
            
            return self.success_response("Success", data=user_data)
    
    @jwt_required()
    def put(self, user_id):
        current_user_identity = get_jwt_identity()
        current_user_role = current_user_identity['role']
        
        if current_user_role != 1:
            return self.error_response("Unauthorized access", 403)
        
        user = tbl_users.query.get(user_id)
        
        if not user:
            return self.error_response("No data user found", 404)
        
        data = request.get_json()
        
        user.email = data.get('email')
        user.user_name = data.get('user_name')
        user.password = data.get('password')
        user.role = data.get('role'),
        user.status = data.get('status')
        
        db.session.commit()
        
        return self.success_response("user data has been Updated Successfully")
    
    @jwt_required()
    def patch(self,user_id):
        currrent_user_identity = get_jwt_identity()
        current_user_role = current_user_identity['role']
        
        if current_user_role != 1:
            return self.error_response("unauthorized access", 403)
        
        user = tbl_users.query.get(user_id)
        
        if not user:
            return self.error_response("no user found", 404)
        
        data = request.get_json()
        
        if 'email' in data:
            user.email = data['email']
        if 'user_name' in data:
            user.user_name = data['user_name']
        if 'password' in data:
            user.password = data['password']
        if 'role' in data:
            user.role = data['role']
        if 'status' in data:
            user.status = data['status']
            
        db.session.commit()
        
        return self.success_response("user data has been updated successfully")
    
    @jwt_required()
    def delete(self, user_id):
        current_user_identity = get_jwt_identity()
        current_user_role = current_user_identity['role']
        
        if current_user_role != 1:
            return self.error_response("Unauthorized access", 403)
        
        user = tbl_users.query.get(user_id)
        
        if not user:
            return self.error_response("No user found with that id", 404)
                
        db.session.delete(user)
        db.session.commit()
        
        return self.success_response("user data has Delete Successfully")
    
class DeleteAlluserResource(Resource, ResponseHandler):
    @jwt_required()
    def get(self):
        current_user_identity = get_jwt_identity()
        current_user_role = current_user_identity['role']
        
        if current_user_role != 1:
            return self.error_response("Unauthorized access", 403)
        
        users = tbl_users.query.all()
   
        if not users:
            return self.error_response("No Data users found", 404)
        
        db.session.delete(users)
        db.session.commit()    
            
        return self.success_response("all users data has Delete Successfully")

    