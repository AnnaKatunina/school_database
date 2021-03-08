import random
import string


from models import Group, db, Course, Student


def create_groups():

    for _ in range(20):
        group_number = ''.join(random.sample(string.ascii_uppercase, 2)) + '_' + \
                       ''.join(random.sample(string.digits, 2))
        group = Group(name=group_number)
        db.session.add(group)
        db.session.commit()


def create_students():
    first_name_list = ['Oliver', 'Steven', 'Amelia', 'Emily', 'Harry', 'Olivia', 'Jacob', 'Charlie', 'Mary', 'William',
                       'Elizabeth', 'Jennifer', 'Thomas', 'Jessica', 'Margaret', 'Mark', 'Paul', 'Amy', 'Laura', 'Jack']
    last_name_list = ['Smith', 'Jones', 'Taylor', 'Williams', 'Brown', 'White', 'Harris', 'Martin', 'Davies', 'Wilson',
                      'Cooper', 'Evans', 'King', 'Thomas', 'Baker', 'Green', 'Johnson', 'Edwards', 'Clark', 'Lewis']

    for _ in range(200):
        first_name = random.choice(first_name_list)
        last_name = random.choice(last_name_list)
        group = random.randint(1, 20)
        student = Student(first_name=first_name, last_name=last_name, group_id=group)
        db.session.add(student)
        db.session.commit()


def create_courses():
    courses_dict = {'Math': 'Encompasses a growing variety and depth of subjects over history, and comprehension'
                            'of it requires a system to categorize and organize these various subjects into a more'
                            'general areas of mathematics',
                    'Biology': 'The natural science that studies life and living organisms, including their physical'
                               'structure, chemical processes, molecular interactions, physiological mechanisms,'
                               'development and evolution',
                    'Chemistry': 'The scientific discipline involved with elements and compounds composed of atoms,'
                                 'molecules and ions',
                    'History': 'The study of the past, relates to past events as well as the memory, discovery,'
                               'collection, organization, presentation, and interpretation of information about'
                               'these events',
                    'Physics': 'The natural science that studies matter, its motion and behavior through space and'
                               'time, and the related entities of energy and force.',
                    'Economics': 'The social science that studies how people interact with value; in particular,'
                                 'the production, distribution, and consumption of goods and services',
                    'Computing': 'The study and experimentation of algorithmic processes and development of both'
                                 'hardware and software.',
                    'English': ' The study of literature, the majority of which comes from Britain and the United'
                               'States; English composition, English grammar and style; English sociolinguistics.',
                    'Algebra': 'The study of algebraic structures, which are sets and operations defined'
                               'on these sets satisfying certain axioms.',
                    'Geometry': 'Initially the study of spatial figures like circles and cubes,'
                                'though it has been generalized considerably.'
                    }
    for course in courses_dict:
        one_course = Course(name=course, description=courses_dict[course])
        db.session.add(one_course)
        db.session.commit()


# create_groups()
# create_courses()
# create_students()
