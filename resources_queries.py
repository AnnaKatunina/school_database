from flask import jsonify, request, make_response
from flask_restful import Resource, reqparse
from sqlalchemy import func

from db_and_models import Group, session, Student, Course, students_courses


class GetGroups(Resource):

    def get(self):
        number_of_students_param = request.args.get('number_of_students', type=int)
        groups = session.query(Group, func.count(Student.group_id)).join(Student, Group.id == Student.group_id). \
            group_by(Group.id, Group.name).order_by(Group.id).all()
        if number_of_students_param:
            groups = session.query(Group, func.count(Student.group_id)).join(Student, Group.id == Student.group_id).\
                having(func.count(Student.group_id) <= number_of_students_param).group_by(Group.id, Group.name).\
                order_by(func.count(Student.group_id).desc()).all()
        all_groups = []
        for group in groups:
            group_dict = {
                'id': group[0].id,
                'name': group[0].name,
                'number_of_students': group[1],
            }
            all_groups.append(group_dict)
        return jsonify(all_groups)


class GetStudents(Resource):

    def get(self):
        course_name_param = request.args.get('course_name', type=str)
        students = session.query(Student).all()
        if course_name_param:
            course_id_by_name = session.query(Course.id).filter(Course.name == course_name_param.title()).first()
            students = session.query(Student).join(students_courses, Student.id == students_courses.columns.student_id).\
                filter(students_courses.columns.course_id == course_id_by_name).all()
        all_students = []
        for student in students:
            student_dict = {
                'id': student.id,
                'first_name': student.first_name,
                'last_name': student.last_name,
                'group_id': student.group_id,
                'courses': [course.name for course in student.courses],
            }
            all_students.append(student_dict)
        return jsonify(all_students)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('first_name', type=str, required=True)
        parser.add_argument('last_name', type=str, required=True)
        parser.add_argument('group_id', type=str, required=False)
        data = parser.parse_args()
        new_student = Student(first_name=data['first_name'], last_name=data['last_name'], group_id=data['group_id'])
        session.add(new_student)
        session.commit()
        student_dict = {
            'id': new_student.id,
            'first_name': new_student.first_name,
            'last_name': new_student.last_name,
            'group_id': new_student.group_id,
            }
        return make_response(jsonify(student_dict), 201)

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('first_name', type=str, required=True)
        parser.add_argument('last_name', type=str, required=True)
        data = parser.parse_args()
        student = session.query(Student).filter_by(first_name=data['first_name'], last_name=data['last_name']).one()
        session.delete(student)
        session.commit()
        return make_response(f"Student {data['first_name']} {data['last_name']}was deleted", 204)


class GetCourses(Resource):

    def get(self):
        courses = session.query(Course).all()
        all_courses = []
        for course in courses:
            course_dict = {
                'id': course.id,
                'name': course.name,
                'description': course.description,
                'students': [f"{student.id} {student.first_name} {student.last_name}" for student in course.students],
            }
            all_courses.append(course_dict)
        return jsonify(all_courses)

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id_course', type=int, required=True)
        parser.add_argument('id_student', type=int, required=True)
        data = parser.parse_args()
        new_student_in_course = students_courses.insert().values(student_id=data['id_student'],
                                                                 course_id=data['id_course'])
        session.execute(new_student_in_course)
        session.commit()
        course = session.query(Course).get(data['id_course'])
        course_dict = {
            'id': course.id,
            'name': course.name,
            'description': course.description,
            'students': [f"{student.id} {student.first_name} {student.last_name}" for student in course.students],
        }
        return make_response(jsonify(course_dict), 201)

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('course_id', type=int, required=True)
        parser.add_argument('student_id', type=int, required=True)
        data = parser.parse_args()
        student = students_courses.delete().where(students_courses.columns.course_id == data['course_id']).\
            where(students_courses.columns.student_id == data['student_id'])
        session.execute(student)
        session.commit()
        course = session.query(Course).get(data['course_id'])
        course_dict = {
            'id': course.id,
            'name': course.name,
            'description': course.description,
            'students': [f"{student.id} {student.first_name} {student.last_name}" for student in course.students],
        }
        return jsonify(course_dict)
