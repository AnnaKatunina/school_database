An application that inserts/updates/deletes data in the database using Sqlalchemy and Flask REST API framework.

Database has 3 tables:
- Groups
- Courses
- Students

The application accepts the following requests:

1. /api/v1/groups - all groups with numbers of students. GET method has an optional parameter "number_of_students", it returns groups less than or equal to parameter's value.

2. /api/v1/students - all students with their group and list of courses. GET method has an optional parameter "course_name", it returns all students who has this parameter's value in their list of courses.
In the POST method and DELETE method you can add new new student or remove existing student.

3. /api/v1/courses - all courses with their description and list of students who are enrolled in this course.
Using the POST method you can enroll a student in a course and using the DELETE method you can remove a student from the course.
