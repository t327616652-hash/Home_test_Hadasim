from typing import List
from fastapi import FastAPI, Depends, HTTPException, Header
from sqlalchemy.orm import Session
import models, schemas, database
from fastapi.middleware.cors import CORSMiddleware



# there are 60 minutes in a degree
MINUTES_IN_A_DEGREE = 60
# there are 3600 seconds in a degree
SECONDS_IN_A_DEGREE = 3600


# create the database
models.Base.metadata.create_all(bind = database.engine)

# init app
app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)



''' add_teacher - adding a new teacher to the database. 
      the method:
         expects to receive information of the type based on the schemas.Teacher model
         uses the session created in the database.py file because information needs to be transferred into the database '''

@app.post('/teachers/')
def add_teacher(teacher: schemas.TeacherCreate, db: Session = Depends(database.get_db)):
    # checking if the teacher already exists in the database
   already_exists = db.query(models.Teacher).filter(teacher.id == models.Teacher.id).first()

    # if the teacher already exists in the database
   if already_exists:
       # exception (of code 400 - bad bequest)
       raise HTTPException(status_code = 400, detail = "This ID already exists in the system!")

   # creates a teacher record
   db_teacher = models.Teacher()
   # initializes the data of the new teacher
   db_teacher.id = teacher.id
   db_teacher.full_name = teacher.full_name
   db_teacher.class_number = teacher.class_number

   # adds the new record (db_teacher) to the database
   db.add(db_teacher)
   # performs the operation
   db.commit()
   # allows to get back the record that has just been added
   db.refresh(db_teacher)

   return {"message": f"Teacher {db_teacher.full_name} added successfully"}








''' add_student - adding a new student to the database. 
      the method:
         expects to receive information of the type based on the schemas.Student model
         uses the session created in the database.py file because information needs to be transferred into the database '''

@app.post('/students/')
def add_student(student: schemas.StudentCreate, db: Session = Depends(database.get_db)):
    # checking if the student already exists in the database
   already_exists = db.query(models.Student).filter(student.id == models.Student.id).first()

    # if the student already exists in the database
   if already_exists:
       # exception (of code 400 - bad bequest)
       raise HTTPException(status_code = 400, detail = "This ID already exists in the system!")

   # creates a student record and initializes the data of the new teacher
   db_student = models.Student(**student.model_dump())
   '''# initializes the data of the new teacher
   db_student.id = student.id
   db_student.full_name = student.full_name
   db_student.class_number = student.class_number'''

   # adds the new record (db_student) to the database
   db.add(db_student)
   # performs the operation
   db.commit()
   # allows to get back the record that has just been added
   db.refresh(db_student)

   return {"message": f"Student {db_student.full_name} added successfully"}







''' update_location - updating a new location. 
      the method:
         expects to receive information of the type based on the schemas.Location model
         uses the session created in the database.py file because information needs to be transferred into the database '''

@app.post('/location/')
def update_location(location_data: schemas.Location, db: Session = Depends(database.get_db)):
    # the longitude and latitude of the location that received
    longitude = location_data.Coordinates.Longitude
    latitude = location_data.Coordinates.Latitude

    # the converted to decimal longitude and latitude of the location that received
    decimal_longitude = convert_dms_to_decimal(longitude.Degrees, longitude.Minutes, longitude.Seconds)
    decimal_latitude = convert_dms_to_decimal(latitude.Degrees, latitude.Minutes, latitude.Seconds)

    # checking if the student's location already exists in the database
    db_location = db.query(models.Location).filter(models.Location.student_id == location_data.ID).first()

    # if the student's location already exists - just update it
    if db_location:
        db_location.longitude = decimal_longitude
        db_location.latitude = decimal_latitude
        db_location.time = location_data.Time
    else:
        # creates a location record and initializes the data of the new location
        db_location = models.Location(student_id=location_data.ID,
                                       longitude=decimal_longitude,
                                       latitude=decimal_latitude,
                                       time=location_data.Time)

    # adds the new record (new_location) to the database
    db.add(db_location)
    # performs the operation
    db.commit()
    # allows to get back the record that has just been added
    db.refresh(db_location)

    return {"message": "Location updated"}








''' get_locations - returns a list of all the locations
      the method:
         uses the session created in the database.py file because information needs to be transferred into the database '''

@app.get("/locations")
def get_locations(db: Session = Depends(database.get_db)):
    return db.query(models.Location).all()








''' get_all_teachers - returns a list of all the teachers
      the method:
         expects to receive a teacher's id of the type str
         uses the session created in the database.py file because information needs to be transferred into the database '''

@app.get('/teachers/', response_model = List[schemas.Teacher])
def get_all_teachers(teacher_id: str = Header(...), db: Session = Depends(database.get_db)):
    # checking if the attempt to access the data is by a teacher
    is_teacher(teacher_id, db)

    # if it is (means no exception appeared) it returns the list of teachers
    return db.query(models.Teacher).all()








''' get_all_students - returns a list of all the students
      the method:
         expects to receive a teacher's id of the type str
         uses the session created in the database.py file because information needs to be transferred into the database '''

@app.get('/students/', response_model = List[schemas.Student])
def get_all_students(teacher_id: str = Header(...), db: Session = Depends(database.get_db)):
    # checking if the attempt to access the data is by a teacher
    is_teacher(teacher_id, db)

    # if it is (means no exception appeared) it returns the list of students
    return db.query(models.Student).all()








''' get_student - returns a student if exists, otherwise raises an exception
      the method:
         expects to receive an id of a student (to search) and a teacher's id of the type str
         uses the session created in the database.py file because information needs to be transferred into the database '''

@app.get('/students/{id}', response_model = schemas.Student)
def get_student(id: str, teacher_id: str = Header(...), db: Session = Depends(database.get_db)):
    # checking if the attempt to access the data is by a teacher
    is_teacher(teacher_id, db)

    # student will contain the student detail if the id exists in the student's database
    student = db.query(models.Student).filter(id == models.Student.id).first()

    # if this student doesn't exist
    if not student:
        # exception (of code 404 - can not find the requested source)
        raise HTTPException(status_code = 404, detail = "This student does not exist!")

    # if it is (means no exception appeared) it returns the student
    return student








''' get_teacher - returns a teacher if exists, otherwise raises an exception
      the method:
         expects to receive an id of a teacher (to search) and a teacher's id of the type str
         uses the session created in the database.py file because information needs to be transferred into the database '''

@app.get('/teachers/{id}', response_model = schemas.Teacher)
def get_teacher(id: str, teacher_id: str = Header(...), db: Session = Depends(database.get_db)):
    # checking if the attempt to access the data is by a teacher
    is_teacher(teacher_id, db)

    # teacher will contain the teacher detail if the id exists in the teacher's database
    teacher = db.query(models.Teacher).filter(id == models.Teacher.id).first()

    # if this teacher doesn't exist
    if not teacher:
        # exception (of code 404 - can not find the requested source)
        raise HTTPException(status_code = 404, detail = "This teacher does not exist!")

    # if it is (means no exception appeared) it returns the teacher
    return teacher








''' get_teacher - returns the list of all the students in the class
      the method:
         expects to receive an id of a class number of type int and a teacher's id of the type str
         uses the session created in the database.py file because information needs to be transferred into the database '''

@app.get('/students/class/{class_number}', response_model=List[schemas.Student])
def get_all_students_in_class(teacher_id: str = Header(...), db: Session = Depends(database.get_db)):
    # checking if the attempt to access the data is by a teacher
    is_teacher(teacher_id, db)

    # loading the teachers' details
    teacher = db.query(models.Teacher).filter(teacher_id == models.Teacher.id).first()
    # the teacher's class number
    class_number = teacher.class_number

    # returns all the students in this teacher's class
    return db.query(models.Student).filter(class_number == models.Student.class_number).all()









''' is_teacher - verifying if the attempt to access the data is by a teacher
                 if it's not a teacher than it raises an exception
      the method:
         expects to receive a teacher's id of the type str
         uses the session created in the database.py file because information needs to be transferred into the database '''

def is_teacher(teacher_id: str, db: Session):
    # checking if the id is of a teacher
    teacher = db.query(models.Teacher).filter(teacher_id == models.Teacher.id).first()
    # if it's not a teacher trying to reach the data...
    if not teacher:
        # exception (of code 403 - the server refuses to authorize the request)
        raise HTTPException(status_code = 403, detail = "Access is blocked - you are not a teacher!")








''' convert_dms_to_decimal - converting DMS to decimal.
      the method expects to receive the DMS = degrees, minutes and seconds.'''

def convert_dms_to_decimal(degrees: int, minutes: int, seconds: int) -> float:
    # the formula to convert DMS to decimal
    decimal = degrees + (minutes / MINUTES_IN_A_DEGREE) + (seconds / SECONDS_IN_A_DEGREE)
    return decimal








if __name__ == '__main__':
   print("")