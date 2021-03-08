from flask_sqlalchemy import SQLAlchemy

from main_app import app

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://admin:admin1234@localhost:5432/school"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


students_courses = db.Table('students_courses',
                            db.Column('student_id', db.Integer, db.ForeignKey('student.id')),
                            db.Column('course_id', db.Integer, db.ForeignKey('course.id'))
                            )


class Group(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('group.id'))
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    courses = db.relationship('Course', secondary='students_courses', lazy='dynamic', backref=db.backref('students'))


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    description = db.Column(db.String())
    students = db.relationship('Student', secondary='students_courses', lazy='dynamic', backref=db.backref('courses'))


# db.create_all()
