from flask import Flask, request, jsonify
from flask import json
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token, create_refresh_token
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from app.config import Config
from app.models.model import db, tbl_users, tbl_students
from app.utils.additional_handler import ResponseHandler

app = Flask(__name__)
api = Api(app)
CORS(app)

# Use configuration from config.py
app.config.from_object(Config)

jwt = JWTManager(app)
bcrypt = Bcrypt(app)
# Initialize the SQLAlchemy instance with the app context
db.init_app(app)

ROLES = ['teacher','parent','student'];


# Resource for retrieving student information
class get(Resource):
    def get(self):
        return "<h1>Welcome Visitor<h1><br><br><center>-Sekolah Bersama-<center>"

# tbl_users registration endpoint
class register(Resource, ResponseHandler):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        role = data.get('role')
        status = data.get('status')

        if tbl_users.query.filter_by(user_name=username).first():
            return self.error_response("tbl_users already exists", 400)

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = tbl_users(email=email,user_name=username, password=hashed_password, role=role,status=status)
        db.session.add(new_user)
        db.session.commit()
        
        return self.success_response("tbl_users registered successfully")



# tbl_users login endpoint
class login(Resource, ResponseHandler):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')

        user = tbl_users.query.filter_by(email=email).first()

        if not user or not bcrypt.check_password_hash(user.password, password):
            return self.error_response("Invalid credentials", 401)

        # Generate JWT token
        identity = {'username': username, 'email': email, 'role': user.role}
        access_token = create_access_token(identity=identity)
        refresh_token = create_refresh_token(identity=identity)
        return self.success_response(
            "Login successful",
            access_token=access_token,
            refresh_token=refresh_token
            )
    
class refresh(Resource, ResponseHandler):
    @jwt_required(refresh=True)
    def post(self):
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        return self.success_response(
            "Refresh successful",
                access_token=access_token
            )
                
