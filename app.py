from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from schemas import (
    UserAuth,
    UserOut,
    TokenSchema,
    StudentCreate,
    StudentOut
)

from utils import (
    get_hashed_password,
    create_access_token,
    create_refresh_token,
    verify_password
)

from uuid import uuid4

app = FastAPI(title="Student Management System")

users_db = {}
students_db = {}

@app.post("/signup", response_model=UserOut)
async def create_user(data: UserAuth):

    user = users_db.get(data.email)

    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )

    user = {
        "id": str(uuid4()),
        "username": data.username,
        "email": data.email,
        "password": get_hashed_password(data.password)
    }

    users_db[data.email] = user

    return UserOut(
        id=user["id"],
        username=user["username"],
        email=user["email"]
    )


@app.post("/login", response_model=TokenSchema)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends()
):

    user = users_db.get(form_data.username)

    if not user:
        raise HTTPException(
            status_code=400,
            detail="User not found"
        )

    if not verify_password(
        form_data.password,
        user["password"]
    ):
        raise HTTPException(
            status_code=400,
            detail="Incorrect password"
        )

    return {
        "access_token": create_access_token(user["email"]),
        "refresh_token": create_refresh_token(user["email"]),
        "token_type": "bearer"
    }


@app.get("/users", response_model=list[UserOut])
async def get_users():

    return [
        {
            "id": user["id"],
            "username": user["username"],
            "email": user["email"]
        }
        for user in users_db.values()
    ]

@app.post("/students", response_model=StudentOut)
async def create_student(student: StudentCreate):

    student_id = str(uuid4())

    new_student = {
        "id": student_id,
        "name": student.name,
        "age": student.age,
        "course": student.course,
        "email": student.email
    }

    students_db[student_id] = new_student

    return new_student


@app.get("/students", response_model=list[StudentOut])
async def get_students():

    return list(students_db.values())


@app.get("/students/{student_id}", response_model=StudentOut)
async def get_student(student_id: str):

    student = students_db.get(student_id)

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student


@app.put("/students/{student_id}", response_model=StudentOut)
async def update_student(
    student_id: str,
    student: StudentCreate
):

    existing_student = students_db.get(student_id)

    if not existing_student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    updated_student = {
        "id": student_id,
        "name": student.name,
        "age": student.age,
        "course": student.course,
        "email": student.email
    }

    students_db[student_id] = updated_student

    return updated_student


@app.delete("/students/{student_id}")
async def delete_student(student_id: str):

    student = students_db.get(student_id)

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    del students_db[student_id]

    return {
        "message": "Student deleted successfully"
    }