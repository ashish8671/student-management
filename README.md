# Student Management System

## Overview

A simple Student Management System built using FastAPI, SQLite, SQLAlchemy, and JWT Authentication.

### Features

* User Registration
* User Login
* JWT Token Generation
* Add Student
* View Students
* Update Student
* Delete Student

---

## Technologies Used

* FastAPI
* SQLite
* SQLAlchemy
* JWT
* Pydantic

---

## Project Structure

```text
student_management/
│
├── main.py
├── database.py
├── models.py
├── schemas.py
├── auth.py
├── crud.py
└── students.db
```

---

## Database Tables

### User

```text
id
username
password
```

### Student

```text
id
name
age
course
email
```

---

## Pseudocode

### User Registration

```text
Receive username and password

Hash password

Create User object

Save user in database

Return success response
```

---

### User Login

```text
Receive username and password

Find user in database

Verify password

Generate JWT token

Return token
```

---

### Add Student

```text
Receive student details

Create Student object

Save into database

Return student information
```

---

### View Students

```text
Fetch all student records

Return list of students
```

---

### Update Student

```text
Find student by ID

Update student details

Save changes

Return updated student
```

---

### Delete Student

```text
Find student by ID

Delete record

Commit changes

Return success message
```

---

## API Endpoints

| Method | Endpoint       | Description    |
| ------ | -------------- | -------------- |
| POST   | /register      | Register User  |
| POST   | /login         | Login User     |
| POST   | /students      | Add Student    |
| GET    | /students      | View Students  |
| PUT    | /students/{id} | Update Student |
| DELETE | /students/{id} | Delete Student |

---

## How to Run

```bash
pip install fastapi uvicorn sqlalchemy python-jose

fastapi dev main.py
```

Open:

```text
http://127.0.0.1:8000/docs
```

---

## Conclusion

This project implements a Student Management System using FastAPI and SQLite. It provides JWT-based authentication and supports CRUD operations for managing student records.
