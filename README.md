## Home_test_Hadasim
# School Trip Management System - Bnot Moshe school
A project for recruitment for the Hadasim program - a full-stack solution for managing school trips, including teacher/student registration and real-time location monitoring. 

## Features

- **Full-Stack Architecture**: Separation of concerns between Client (Frontend) and Server (Backend).
- **User Management**: 
  - Registration for both Teachers and Students.
  - Data validation for ID numbers.
- **Robust API**: RESTful API built with FastAPI that provides endpoints for retrieving and serving data.
- **Relational Database**: Persistent storage using SQLite with a structured schema for Teachers and Students.
- **Specific queries (only accessible to teachers by ID)**: 
  - Retrieve all registered users (retrieve all teachers or retrieve all students).
  - Retrieve specific details of a teacher/student by ID.
  - Retrieve all students based on their class (specific view of the students in the class for the class teacher).
- **Real-Time Location Tracking**:
  - Students' devices send GPS coordinates (DMS format) to the server. 
  - Automatic conversion from DMS (Degrees, Minutes, Seconds) to Decimal format. 
  - **Live Map**: Interactive Map (Leaflet.js) showing the current location of all students. 
  - **Upsert Logic**: The database maintains only the most recent location for each student to ensure performance and clarity.

## Prerequisites

- Python 3.7+
- pip (Python package manager)

## Installation

1. **Clone the project:**
   ```bash
   git clone https://github.com/t327616652-hash/Home_test_Hadasim
   cd Home_test_Hadasim
   ```

2. **Create a virtual environment (in server):**
   ```bash
   cd server
   python3 -m venv venv
   ```

3. **Activate the virtual environment:**
   ```bash
   # On macOS/Linux:
   source venv/bin/activate
   
   # On Windows:
   venv\Scripts\activate
   ```

## Running the Server
### Start the FastAPI server using Uvicorn:

### Manual Start

1. **Activate the virtual environment** (if not already activated):
   ```bash
   # On macOS/Linux:
   source venv/bin/activate
   
   # On Windows:
   venv\Scripts\activate
   ```

2. **Start the FastAPI server from the project root:**
   ```bash
   uvicorn Server.main:app --reload
   ```

   The `--reload` flag enables auto-reload on code changes.

3. **View the Map**:

   Open client/map.html in any web browser.


**The server will be available at:**
   - API: `http://127.0.0.1:8000
   - Interactive API Documentation: `http://127.0.0.1:8000/docs`
   - Alternative API Documentation: `http://127.0.0.1:8000/redoc`

## API Endpoints

---

### 1. User Registration

**POST** `/teachers`

Register a new user (teacher) with ID, full name (first + last names) and class number.

**Parameters:**

Teacher (schemas.Teacher) contins:
- `id` (string, required): The ID of the teacher (must be of 9 digits).
- `full_name` (string, required): The teacher's full name.
- `class_number` (int, required): The class number that the teacher teaches at.

**Success Response:**
```json
{
  "message": "Teacher Tal Ramon added successfully"
}
```

**Error Responses:**
```json
{
  "detail": "This ID already exists in the system!"
}
```

```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": [
        "body",
        "id"
      ],
      "msg": "Value error, ID must contain only digits",
      "input": "12345678g",
      "ctx": {
        "error": {}
      }
    }
  ]
}
```

```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": [
        "body",
        "id"
      ],
      "msg": "String should have at least 9 characters",
      "input": "123",
      "ctx": {
        "min_length": 9
      }
    }
  ]
}
```

```json
{
  "detail": [
    {
      "type": "string_too_long",
      "loc": [
        "body",
        "id"
      ],
      "msg": "String should have at most 9 characters",
      "input": "1234567890",
      "ctx": {
        "max_length": 9
      }
    }
  ]
}
```



**POST** `/students`

Register a new user (student) with ID, full name (first + last names) and class number.

**Parameters:**

Student (schemas.Student) contins:
- `id` (string, required): The ID of the student (must be of 9 digits).
- `full_name` (string, required): The student's full name.
- `class_number` (int, required): The class number that the student studies at.

**Success Response:**
```json
{
  "message": "Student Dana Mendes added successfully"
}
```

**Error Responses:**
```json
{
  "detail": "This ID already exists in the system!"
}
```

```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": [
        "body",
        "id"
      ],
      "msg": "Value error, ID must contain only digits",
      "input": "12345678g",
      "ctx": {
        "error": {}
      }
    }
  ]
}
```

```json
{
  "detail": [
    {
      "type": "string_too_short",
      "loc": [
        "body",
        "id"
      ],
      "msg": "String should have at least 9 characters",
      "input": "123",
      "ctx": {
        "min_length": 9
      }
    }
  ]
}
```

```json
{
  "detail": [
    {
      "type": "string_too_long",
      "loc": [
        "body",
        "id"
      ],
      "msg": "String should have at most 9 characters",
      "input": "1234567890",
      "ctx": {
        "max_length": 9
      }
    }
  ]
}
```



### 2. Data Retrieval

**GET** `/teachers/`

Returns a list of all teachers (available only for teachers).

**Parameters:**
- `teacher_id` (string, required): The teacher ID in order to allow the access to the data.

**Success Response:**

The list of all the teachers (each one is like):
```json
[
  {
    "id": "string",
    "full_name": "string",
    "class_number": 0
  }
]
```

**Error Responses:**
```json
{
  "detail": "Access is blocked - you are not a teacher!"
}
```



**GET** `/students/`

Returns a list of all students (available only for teachers).

**Parameters:**
- `teacher_id` (string, required): The teacher ID in order to allow the access to the data.

**Success Response:**

The list of all the students (each one is like):
```json
[
  {
    "id": "string",
    "full_name": "string",
    "class_number": 0
  }
]
```

**Error Responses:**
```json
{
  "detail": "Access is blocked - you are not a teacher!"
}
```



**GET** `/teachers/{id}`

Returns a teacher (available only for teachers).

**Parameters:**
- `teacher_id` (string, required): The teacher ID in order to allow the access to the data.

**Success Response:**

A teacher details:
```json
[
  {
    "id": "string",
    "full_name": "string",
    "class_number": 0
  }
]
```

**Error Responses:**
```json
{
  "detail": "Access is blocked - you are not a teacher!"
}
```




**GET** `/students/{id}`

Returns a student (available only for teachers).

**Parameters:**
- `teacher_id` (string, required): The teacher ID in order to allow the access to the data.

**Success Response:**

A student details:
```json
[
  {
    "id": "string",
    "full_name": "string",
    "class_number": 0
  }
]
```

**Error Responses:**
```json
{
  "detail": "Access is blocked - you are not a teacher!"
}
```



**GET** `/students/class/{class_number}`

Returns a list of all the students in the class (available only for the teacher how teaches that class).

**Parameters:**
- `teacher_id` (string, required): The teacher ID in order to allow the access to the data.

**Success Response:**

A list of all the students in class (each is like):
```json
[
  {
    "id": "string",
    "full_name": "string",
    "class_number": 0
  }
]
```

**Error Responses:**
```json
{
  "detail": "Access is blocked - you are not a teacher!"
}
```

### 3. Location Management
**POST** `/locations`

Updates or inserts the current location of a student.

**Parameters:** Student ID, Time, and Coordinates in DMS (Degrees, Minutes, Seconds).
**Logic:** Logic: Converts coordinates to Decimal and updates the locations table.

**Success Response:**
```json
{
  "message": "Location updated"
}
```


**GET** `/locations/`

Returns the list of the most recent locations for all students to be displayed on the map.


## Project Structure
### School Trip Management System - Bnot Moshe school

```
Home_test_Hadasim/
├── Server/
│   ├── database.py        # SQLite connection setup
│   ├── models.py          # SQLAlchemy models (Teachers, Students, Locations)
│   ├── schemas.py         # Pydantic validation schemas
│   ├── main.py            # FastAPI routes & logic
│   ├── Users.json         # User data (for attack scripts)
│   └── school.db          # SQLite database file
├── client/
│   ├── map.html           # Leaflet.js Map Frontend       
├── README.md              # This file
└── venv/                  # Virtual environment (created after setup)
```

---


## ScreenShots - in a folder here in the project