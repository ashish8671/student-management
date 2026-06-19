from fastapi import FastAPI, status, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from database import users_collection, students_collection
from bson import ObjectId
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

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

users_db = {}
students_db = {}

@app.get("/", include_in_schema=False)
async def root():
    return RedirectResponse(url="/docs")

@app.post("/signup", response_model=UserOut)
async def create_user(data: UserAuth):

    existing_user = users_collection.find_one(
        {"email": data.email}
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="User already exists"
        )

    user = {
        "username": data.username,
        "email": data.email,
        "password": get_hashed_password(data.password)
    }

    result = users_collection.insert_one(user)

    return {
        "id": str(result.inserted_id),
        "username": data.username,
        "email": data.email
    }

@app.post("/login", response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):

    user = users_collection.find_one(
        {"email": form_data.username}
    )

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

    new_student = {
        "name": student.name,
        "age": student.age,
        "course": student.course,
        "email": student.email
    }

    result = students_collection.insert_one(new_student)

    return {
        "id": str(result.inserted_id),
        "name": student.name,
        "age": student.age,
        "course": student.course,
        "email": student.email
    }

@app.get("/students")
async def get_students():

    students = []

    for student in students_collection.find():

        students.append({
            "id": str(student["_id"]),
            "name": student["name"],
            "age": student["age"],
            "course": student["course"],
            "email": student["email"]
        })

    return students

@app.get("/students/{student_id}")
async def get_student(student_id: str):

    student = students_collection.find_one(
        {"_id": ObjectId(student_id)}
    )

    if not student:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return {
        "id": str(student["_id"]),
        "name": student["name"],
        "age": student["age"],
        "course": student["course"],
        "email": student["email"]
    }
@app.put("/students/{student_id}")
async def update_student(
    student_id: str,
    student: StudentCreate
):
    result = students_collection.update_one(
        {"_id": ObjectId(student_id)},
        {
            "$set": {
                "name": student.name,
                "age": student.age,
                "course": student.course,
                "email": student.email
            }
        }
    )

    if result.modified_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return {
        "message": "Student updated successfully"
    }
@app.delete("/students/{student_id}")
async def delete_student(student_id: str):

    result = students_collection.delete_one(
        {"_id": ObjectId(student_id)}
    )

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return {
        "message": "Student deleted successfully"
    }