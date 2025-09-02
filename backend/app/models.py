from sqlmodel import Field, SQLModel, Relationship
from pydantic import EmailStr
from datetime import datetime


# Creating User models

# Admin User model
class Admin(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: EmailStr = Field(nullable=False, unique=True, primary_key=True)
    phone: str = Field(max_length=15)
    password: str
    created_on: datetime = Field(default_factory=datetime.now)
    schools : list["School"] = Relationship(back_populates="admin", cascade_delete=True)
    # add School, Students and Teacher users created list. CASCADE DELETE
    
# School User model
class School(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: EmailStr
    phone: str = Field(max_length=15)
    password: str
    created_on: datetime = Field(default_factory=datetime.now)
    students: list["Student"] = Relationship(back_populates="school", cascade_delete=True)
    teachers: list["Teacher"] = Relationship(back_populates="school", cascade_delete=True)
    admin : Admin = Relationship(back_populates="schools")
    admin_id: int = Field(default=None, foreign_key="admin.id", ondelete="CASCADE")
    

# Teacher SET NULL on attendance list
# Teacher User model
class Teacher(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: EmailStr
    phone: str = Field(max_length=15)
    password: str
    standard : str | None
    section : str | None
    created_on: datetime = Field(default_factory=datetime.now)
    school: School = Relationship(back_populates="teachers")
    school_id: int = Field(default=None, foreign_key="school.id", ondelete="CASCADE")
    
    

# Student User Model
class Student(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    email: EmailStr
    phone: str = Field(max_length=15)
    password: str
    standard : str | None
    section : str | None
    created_on: datetime = Field(default_factory=datetime.now)
    school: School = Relationship(back_populates="students")
    school_id: int = Field(default=None, foreign_key="school.id", ondelete="CASCADE")