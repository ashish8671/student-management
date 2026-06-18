from pydantic import BaseModel, Field, EmailStr


class UserAuth(BaseModel):
    username: str = Field(min_length=3, max_length=30)
    email: EmailStr
    password: str = Field(min_length=6)


class UserOut(BaseModel):
    id: str
    username: str
    email: EmailStr

 
class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class StudentCreate(BaseModel):
    name: str
    age: int
    course: str
    email: EmailStr


class StudentOut(StudentCreate):
    id: str