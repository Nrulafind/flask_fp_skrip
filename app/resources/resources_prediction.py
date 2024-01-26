from flask import Flask, request, jsonify
from flask import json
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token, create_refresh_token
from flask_sqlalchemy import SQLAlchemy

import os
import requests
from flask_cors import CORS
import tensorflow as tf
import ast

from app.config import Config
from app.models.model import db, tbl_users, tbl_students
from app.utils.additional_handler import ResponseHandler

app = Flask(__name__)
api = Api(app)

# Use configuration from config.py
app.config.from_object(Config)

jwt = JWTManager(app)
# Initialize the SQLAlchemy instance with the app context
db.init_app(app)


model_path = './app/utils/score_model.h5'

# Resource for posting predictions
class PostPredictions(Resource, ResponseHandler):
    @jwt_required()
    def post(self):
        current_user_identity = get_jwt_identity()
        current_user_role = current_user_identity['role']

        if current_user_role != 1:
            return self.error_response("Invalid user role", 401)

        if current_user_role == 1: #or (current_user_role == 2 and student_id == 3):
            input_data_str = request.json.get('input_data')
            model = tf.keras.models.load_model(model_path)
            try:
                # print(input_data_str)
                input_data = ast.literal_eval(input_data_str)
                # print(input_data)
                if not isinstance(input_data, list) or len(input_data) != 4:
                    return self.error_response("input_data must contain 4 values in the format [80.5, 90.5, 1.0, 0.1]", 400)

                input_tensor = tf.convert_to_tensor([input_data], dtype=tf.float64)
                output_tensor = model.predict(input_tensor)
                results = output_tensor.tolist()
                return self.success_response("Success", Results=results)
            except Exception as e:
                return self.error_response("Something went wrong", 500)
