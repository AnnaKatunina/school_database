import unittest
import json

from sqlalchemy.orm import sessionmaker

from db_and_models import Base, engine, Student, students_courses
from main_app import app


class CommonTest(unittest.TestCase):

    def setUp(self):
        self.tester = app.test_client()
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.models_to_delete_after_each_test = []


class GroupTest(unittest.TestCase):

    def test_get_all_groups(self):
        tester = app.test_client(self)
        response = tester.get('/api/v1/groups')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertTrue(b'{"id":1,"name":"DG_81","number_of_students":14}' in response.data)

    def test_get_all_groups_with_number_of_students(self):
        tester = app.test_client(self)
        response = tester.get('/api/v1/groups?number_of_students=10')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'{"id":13,"name":"IA_76","number_of_students":9}' in response.data)
        self.assertFalse(b'{"id":1,"name":"DG_81","number_of_students":14}' in response.data)


class StudentTest(CommonTest):

    def tearDown(self):
        for model in self.models_to_delete_after_each_test:
            self.session.delete(model)
            self.session.commit()

    def test_get_all_students(self):
        response = self.tester.get('/api/v1/students')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")
        self.assertTrue(b'{"id":1,"first_name":"Charlie","last_name":"King","group_id":19,'
                        b'"courses":["Algebra","Biology"]}' in response.data)

    def test_get_all_students_with_course_name(self):
        response = self.tester.get('/api/v1/students?course_name=math')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'{"id":16,"first_name":"Paul","last_name":"Thomas","group_id":9,'
                        b'"courses":["Computing","Math"]}' in response.data)
        self.assertFalse(b'{"id":1,"first_name":"Charlie","last_name":"King","group_id":19,'
                         b'"courses":["Algebra","Biology"]}' in response.data)

    def test_add_new_student(self):
        student_test = json.dumps({
            'first_name': 'Test_first_name',
            'last_name': 'Test_last_name'
        })
        response = self.tester.post('/api/v1/students',
                                    headers={"Content-Type": "application/json"},
                                    data=student_test)

        new_student = self.session.query(Student).filter_by(first_name='Test_first_name',
                                                            last_name='Test_last_name').one()
        self.models_to_delete_after_each_test.append(new_student)
        self.assertEqual(response.status_code, 201)
        self.assertTrue(b'"first_name":"Test_first_name","last_name":"Test_last_name"' in response.data)

    def test_delete_student(self):
        student = Student(first_name='Test_delete_first_name', last_name='Test_delete_last_name')
        student_test = json.dumps({
            'first_name': student.first_name,
            'last_name': student.last_name
        })
        self.session.add(student)
        self.session.commit()
        response = self.tester.delete('/api/v1/students',
                                      headers={"Content-Type": "application/json"},
                                      data=student_test)
        self.assertEqual(response.status_code, 204)


class CourseTest(CommonTest):

    def tearDown(self):
        for model in self.models_to_delete_after_each_test:
            student = students_courses.delete().where(students_courses.columns.course_id == model[1]).\
                where(students_courses.columns.student_id == model[0])
            self.session.execute(student)
            self.session.commit()

    def test_get_all_courses(self):
        response = self.tester.get('/api/v1/courses')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, "application/json")

    def test_add_new_student_to_the_course(self):
        student_test = json.dumps({
            'id_course': '10',
            'id_student': '2'
        })
        response = self.tester.post('/api/v1/courses',
                                    headers={"Content-Type": "application/json"},
                                    data=student_test)

        new_student_in_the_course = self.session.query(students_courses).\
            filter(students_courses.columns.course_id == '10',
                   students_courses.columns.student_id == '2').one()
        self.models_to_delete_after_each_test.append(new_student_in_the_course)
        self.assertEqual(response.status_code, 201)

    def test_delete_student_from_the_course(self):
        student_in_course = students_courses.insert().values(student_id=5, course_id=5)
        self.session.execute(student_in_course)
        self.session.commit()
        student_test = json.dumps({
            'student_id': '5',
            'course_id': '5'
        })
        response = self.tester.delete('/api/v1/courses',
                                      headers={"Content-Type": "application/json"},
                                      data=student_test)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
