from pydantic import BaseModel, Field, field_validator


class Student(BaseModel):
    id: str
    full_name: str
    class_number: int

    # this class allows Pydantic to read data from database objects and not just from regular dictionaries.
    class Config:
        from_attributes = True




class StudentCreate(BaseModel):
    # ID must be of length 9
    id: str = Field(..., min_length = 9, max_length = 9)
    full_name: str
    class_number: int

    # checking if the ID received is a number (contains only digits)
    @field_validator('id')
    @classmethod
    def is_numeric(cls, input_id):
        if not input_id.isdigit():
            raise ValueError('ID must contain only digits')
        return input_id







class Teacher(BaseModel):
    id: str
    full_name: str
    class_number: int

    # this class allows Pydantic to read data from database objects and not just from regular dictionaries.
    class Config:
        from_attributes = True




class TeacherCreate(BaseModel):
    # ID must be of length 9
    id: str = Field(..., min_length = 9, max_length = 9)
    full_name: str
    class_number: int

    # checking if the ID received is a number (contains only digits)
    @field_validator('id')
    @classmethod
    def is_numeric(cls, input_id):
        if not input_id.isdigit():
            raise ValueError('ID must contain only digits')
        return input_id





# a coordinate that represents longitude or latitude.
class DMSCoordinate(BaseModel):
    Degrees: int
    Minutes: int
    Seconds: int




# the coordinates that represent the location
class Coordinates(BaseModel):
    Longitude: DMSCoordinate
    Latitude: DMSCoordinate





# current location (and details) received from the positioning device
class Location(BaseModel):
    ID: str
    Coordinates: Coordinates
    Time: str

    # this class allows Pydantic to read data from database objects and not just from regular dictionaries.
    class Config:
        from_attributes = True