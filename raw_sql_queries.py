from sqlalchemy import text

from db_and_models import session


def get_all_groups_with_less_or_equals_student_count():
    statement = text("""
    SELECT public.group.id, public.group.name, COUNT(public.student.group_id)
    FROM public.group 
    JOIN public.student ON public.group.id = student.group_id
    GROUP BY public.group.id, public.group.name
    HAVING COUNT(public.student.group_id) <= 10
    ORDER BY COUNT(public.student.group_id) DESC
                     """)
    result = session.execute(statement)
    for row in result:
        print(row)


def get_all_students_related_to_the_course_with_a_given_name():
    statement_1 = text("""
    SELECT public.course.id
    FROM public.course 
    WHERE public.course.name = 'Math'
                     """)
    result_1 = session.execute(statement_1)
    course_id_by_name = ''
    for row in result_1:
        course_id_by_name = row[0]
    print(course_id_by_name)

    statement_2 = text("""
        SELECT public.student.id, public.student.first_name, public.student.last_name, public.student.group_id
        FROM public.student
        JOIN public.students_courses ON public.student.id = students_courses.student_id
        WHERE students_courses.course_id = '1'
                         """)
    result_2 = session.execute(statement_2)
    for row in result_2:
        print(row)


def add_new_student():
    statement = text("""
        INSERT INTO public.student (first_name, last_name, group_id)
        VALUES ('Jennifer', 'Thomas', '8')
                         """)
    session.execute(statement)
    session.commit()


def delete_student():
    statement = text("""
        DELETE FROM public.student
        WHERE id = 200
                         """)
    session.execute(statement)
    session.commit()


def add_new_student_to_the_course():
    statement = text("""
        INSERT INTO public.students_courses (student_id, course_id)
        VALUES ('4', '8')
                         """)
    session.execute(statement)
    session.commit()


def delete_student_from_the_course():
    statement = text("""
        DELETE FROM public.students_courses
        WHERE student_id = 4 AND course_id = 8
                         """)
    session.execute(statement)
    session.commit()
