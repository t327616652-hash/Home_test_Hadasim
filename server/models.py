from sqlalchemy import Column, Integer, String, Float
from database import Base


class Teacher(Base):
    # defining the name of the teacher's table in the database
    __tablename__ = "teachers"

    # the columns names and their types in the teacher's table
    id = Column(String, primary_key=True)
    full_name = Column(String)
    class_number = Column(Integer)





class Student(Base):
    # defining the name of the student's table in the database
    __tablename__ = "students"

    # the columns names and their types in the student's table
    id = Column(String, primary_key = True)
    full_name = Column(String)
    class_number = Column(Integer)




class Location(Base):
    __tablename__ = "locations"

    student_id = Column(String, primary_key = True)
    # columns for the location
    longitude = Column(Float)
    latitude = Column(Float)
    # column for the time it updated
    time = Column(String)
