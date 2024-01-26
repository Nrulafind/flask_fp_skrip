import os
from datetime import timedelta 

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI', 'mysql://root:Deathnote01?@localhost/sema_api')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'SEMA-API')
    JWT_ACCESS_TOKEN_EXPIRES = os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', timedelta(minutes=30))
    JWT_REFRESH_TOKEN_EXPIRES = os.environ.get('JWT_REFRESH_TOKEN_EXPIRES', timedelta(days=1))