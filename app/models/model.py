from flask import Flask
from flask import json
from flask_sqlalchemy import SQLAlchemy
from app.config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

# Define the User model
class tbl_users(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50))
    user_name = db.Column(db.String(50))
    password = db.Column(db.String(100))
    role = db.Column(db.Integer)
    status = db.Column(db.Integer)

# Define the Student model
class tbl_students(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nisn = db.Column(db.Integer)
    nama = db.Column(db.String(50))
    alamat = db.Column(db.String(255))
    kelas = db.Column(db.String(255))
    attendance_id = db.Column(db.Integer,db.ForeignKey('tbl_attendances.id',ondelete='CASCADE', onupdate='CASCADE'))
    attendance = db.relationship('tbl_attendances',backref='tbl_students',lazy=True)


# Define the Classes model
class tbl_classes(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama_kelas = db.Column(db.String(50))
    wali_kelas = db.Column(db.String(50))
    students = db.relationship('tbl_students', secondary='classes_students', lazy='subquery',
                               backref=db.backref('tbl_classes', lazy=True))

# Define the Teacher model
class tbl_teachers(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nik = db.Column(db.Integer)
    nama = db.Column(db.String(50))
    alamat = db.Column(db.String(255))
    status = db.Column(db.JSON)

# Define the parents model
class tbl_parents(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama = db.Column(db.String(50))
    alamat = db.Column(db.String(255))
    student_id = db.Column(db.Integer, db.ForeignKey('tbl_students.id', ondelete='CASCADE', onupdate='CASCADE'))
    student = db.relationship('tbl_students', backref='tbl_parents', lazy=True)
    
# Define the attendance model    
class tbl_attendances(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date_attendance_in = db.Column(db.TIMESTAMP)
    date_attendance_out = db.Column(db.TIMESTAMP)
    behaviour = db.Column(db.Text)

# Define the semester model
class tbl_semesters(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nama_semester = db.Column(db.String(50))
    mid_grade = db.Column(db.Float)
    end_grade = db.Column(db.Float)
    prediction = db.Column(db.JSON)
    date = db.Column(db.Date)
    student_id = db.Column(db.Integer, db.ForeignKey('tbl_students.id', ondelete='CASCADE', onupdate='CASCADE'))
    teacher_id = db.Column(db.Integer, db.ForeignKey('tbl_teachers.id', ondelete='CASCADE', onupdate='CASCADE'))
    student = db.relationship('tbl_students', backref='tbl_semesters', lazy=True)
    teacher = db.relationship('tbl_teachers', backref='tbl_teachers', lazy=True)
    
# Define the mapping student
classes_students = db.Table('classes_students', 
                            db.Column('classes_id',db.Integer, db.ForeignKey('tbl_classes.id', ondelete='CASCADE', onupdate='CASCADE')),
                            db.Column('students_id',db.Integer, db.ForeignKey('tbl_students.id', ondelete='CASCADE', onupdate='CASCADE')),
)


# Create the application context
with app.app_context():
    # Create the database tables\
    # db.drop_all()
    db.create_all()
