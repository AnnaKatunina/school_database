from sqlalchemy import create_engine, Table, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker

Base = declarative_base()

engine = create_engine('postgresql://admin:admin1234@localhost:5432/school')


students_courses = Table('students_courses',
                         Base.metadata,
                         Column('student_id', Integer, ForeignKey('student.id')),
                         Column('course_id', Integer, ForeignKey('course.id'))
                         )


class Group(Base):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True)
    name = Column(String())
    st = relationship('Student', backref='group', uselist=False)

    def __repr__(self):
        return f'{self.name}'


class Student(Base):
    __tablename__ = 'student'
    id = Column(Integer, primary_key=True)
    group_id = Column(Integer, ForeignKey('group.id'))
    first_name = Column(String())
    last_name = Column(String())
    courses = relationship('Course', secondary='students_courses', lazy='dynamic', backref=backref('students'))

    def __repr__(self):
        return f'{self.id} {self.first_name} {self.last_name}'


class Course(Base):
    __tablename__ = 'course'
    id = Column(Integer, primary_key=True)
    name = Column(String())
    description = Column(String())

    def __repr__(self):
        return f'{self.name}'


Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()
