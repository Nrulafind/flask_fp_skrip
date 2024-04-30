from flask import Flask, request, jsonify
from flask import json
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token, create_refresh_token
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from app.config import Config
from app.models.model import db, tbl_users, tbl_attendances
from app.utils.additional_handler import ResponseHandler

class GetAllAttendanceResource(Resource, ResponseHandler):
    @jwt_required()
    def get(self):
        current_user_identity = get_jwt_identity()
        current_user_role = current_user_identity['role']
        
        if current_user_role != 1:
            return self.error_response("Unauthorized access", 403)
            
        attendances = tbl_attendances.query.all()
            
        if not attendances:
            return self.error_response("No Attendance found", 404)
            
        attendances_data = [{
            "id":attendance.id,
            "date_attendance_in":attendance.date_attendance_in,
            "date_attendance_out":attendance.date_attendance_out,
            "behaviour":attendance.behaviour
        }for attendance in attendances]
            
        return self.success_response("Success",
                                        data=attendances_data,
                                        # id=attendances.id,
                                        # date_attendance_in=attendances.date_attendance_in,
                                        # date_attendance_out=attendances.date_attendance_out,
                                        # behaviour=attendances.behaviour,          
                                    )
 

class PostAttendanceResource(Resource, ResponseHandler):
    @jwt_required()
    def post(self):
        current_user_identity = get_jwt_identity()
        current_user_role = current_user_identity['role']
        
        if current_user_role != 1:
            return self.error_response("Unauthorized access", 403)
        
        data = request.get_json()
        
        new_attendances = tbl_attendances(
            date_attendance_in=data.get('date_attendance_in'),
            date_attendance_out=data.get('date_attendance_out'),
            behaviour=data.get('behaviour')
        )
        
        db.session.add(new_attendances)
        db.session.commit()
        
        return ResponseHandler.self.success_response("attendance insert successfully")
    

class AttendanceResource(Resource, ResponseHandler):
    @jwt_required()
    def get(self, attendance_id=None):
        current_user_identity = get_jwt_identity()
        current_user_role = current_user_identity['role']
        
        if current_user_role != 1:
            return self.error_response("Unauthorized access", status_code=403)
        
        if attendance_id is not None:
            attendance = tbl_attendances.query.get(attendance_id)
            
            if not attendance:
                return self.error_response("No Attendance found", status_code=404)
        
            attendance_data = {
            "id":attendance.id,
            "date_attendance_in":attendance.date_attendance_in,
            "date_attendance_out":attendance.date_attendance_out,
            "behaviour":attendance.behaviour
            }
            
            return self.success_response("Success", 
                                                    data=attendance_data,
                                                    # id=attendance.id
                                                    )
        
    @jwt_required()
    def put(self, attendance_id):
        current_user_identity = get_jwt_identity()
        current_user_role = current_user_identity['role']
        
        if current_user_role != 1:
            return self.error_response("Unauthorized access", 403)
        
        attendance = tbl_attendances.query.get(attendance_id)
        
        if not attendance:
            return self.error_response("No data Attendance found", 404)
        
        data = request.get_json()
        
        attendance.date_attendance_in = data.get('date_attendance_in')
        attendance.date_attendance_out = data.get('date_attendance_out')
        attendance.behaviour = data.get('behaviour')
        
        db.session.commit()
        
        return ResponseHandler.self.success_response("Attendance data has been Updated Successfully")
    
    @jwt_required()
    def patch(self,class_id):
        currrent_user_identity = get_jwt_identity()
        current_user_role = current_user_identity['role']
        
        if current_user_role != 1:
            return self.error_response("unauthorized access", 403)
        
        attendance = tbl_attendances.query.get(class_id)
        
        if not attendance:
            return self.error_response("no attendance found", 404)
        
        data = request.get_json()

        if 'date_attendance_in' in data:
            attendance.date_attendance_in = data['date_attendance_in']
        if 'date_attendance_out' in data:
            attendance.date_attendance_out = data['date_attendance_out']
        if 'behaviour' in data:
            attendance.behaviour = data['behaviour']
            
        db.session.commit()
        
        return ResponseHandler.self.success_response("Attendance data has been updated successfully")
    
    
    @jwt_required()
    def delete(self, attendance_id):
        current_user_identity = get_jwt_identity()
        current_user_role = current_user_identity['role']
        
        if current_user_role != 1:
            return self.error_response("Unauthorized access", 403)
        
        attendance = tbl_attendances.query.get(attendance_id)
        
        if not attendance:
            return self.error_response("No Attendance found with that id", 404)
                
        db.session.delete(attendance)
        db.session.commit()
        
        return ResponseHandler.self.success_response("attendance data has Delete Successfully")

class DeleteAllAttendanceResource(Resource, ResponseHandler):
    @jwt_required()
    def get(self):
        current_user_identity = get_jwt_identity()
        current_user_role = current_user_identity['role']
        
        if current_user_role != 1:
            return self.error_response("Unauthorized access", 403)
        
        attendances = tbl_attendances.query.all()
   
        if not attendances:
            return self.error_response("No Data attendance found", 404)
        
        db.session.delete(attendances)
        db.session.commit()    
            
        return self.success_response("all Attendance data has Delete Successfully")

    