from sqlmodel import Field, SQLModel, Relationship
from pydantic import EmailStr
from datetime import datetime

import uuid

# Creating User models


# Admin User model
class Admin(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    email: EmailStr = Field(nullable=False, unique=True, primary_key=True)
    phone: str = Field(max_length=15)
    password: str
    
    # created_on: datetime = Field(default_factory=datetime.now)
    schools : list["School"] = Relationship(back_populates="created_by", cascade_delete=True) # When we delete admin with code, it will delete related records of School too!
    # add School, Students and Teacher users created list. CASCADE DELETE
    
# School User model
class School(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    email: EmailStr = Field(nullable=False, unique=True, primary_key=True)
    phone: str = Field(max_length=15)
    password: str

#     created_on: datetime = Field(default_factory=datetime.now)
    students: list["Student"] = Relationship(back_populates="school", cascade_delete=True)
    teachers: list["Teacher"] = Relationship(back_populates="school", cascade_delete=True)
    
    
    created_by : Admin = Relationship(back_populates="schools")
    admin_id: uuid.UUID = Field(default=None, foreign_key="admin.id", ondelete="CASCADE") # To delete related school records, if someone delete admin from DB directly.
    
    
    classes: list["ClassSection"] = Relationship(back_populates="school", cascade_delete=True)
    # feeplan_ids : uuid.UUID = Field(default=None, foreign_key="feeplan.id")
    # feeplans : list["FeePlan"] = Relationship(back_populates="school")
    # feerecords : list["FeeRecord"] = Relationship(back_populates="school")
    

# Teacher SET NULL on attendance list
# Teacher User model
class Teacher(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    email: EmailStr = Field(nullable=False, unique=True, primary_key=True)
    phone: str = Field(max_length=15)
    password: str
# #     standard : str | None
# #     section : str | None
# #     created_on: datetime = Field(default_factory=datetime.now)
    school: School = Relationship(back_populates="teachers")
    school_id: uuid.UUID = Field(default=None, foreign_key="school.id", ondelete="CASCADE")
    classsection : list["ClassSection"] = Relationship(back_populates="classteacher")
#     # attendances : list["Attendance"] = Relationship(back_populates="teacher")
    
    

# Student User Model
class Student(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    # email: EmailStr = Field(nullable=False, unique=True, primary_key=True)
    email: EmailStr = Field(nullable=False, unique=True)
    phone: str = Field(max_length=15)
    password: str
# #     standard : str | None
# #     section : str | None
# #     created_on: datetime = Field(default_factory=datetime.now)
    school: School = Relationship(back_populates="students")
    school_id: uuid.UUID = Field(default=None, foreign_key="school.id", ondelete="CASCADE")
    classsection : "ClassSection" = Relationship(back_populates="students", passive_deletes=True)
    classsection_id: uuid.UUID = Field(foreign_key="classsection.id", ondelete="CASCADE")
#     # attendances : list["Attendance"] = Relationship(back_populates="student")
#     # feerecords : list["FeeRecord"] = Relationship(back_populates="student")


# Class model
class ClassSection(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    school: School = Relationship(back_populates="classes")
    school_id: uuid.UUID = Field(default=None, foreign_key="school.id", ondelete="CASCADE")
    classname: str
    classteacher : Teacher = Relationship(back_populates="classsection")
    classteacher_id: uuid.UUID = Field(default=None, foreign_key = "teacher.id", ondelete="CASCADE")
    # feeplan : "FeePlan" = Relationship(back_populates="classsection")
    students : list["Student"] = Relationship(back_populates="classsection", passive_deletes=True)
    

# Attendance Record
# class Attendance(SQLModel, table=True):
#     id : uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
#     timestamp : datetime 
#     student : Student = Relationship(back_populates="attendances")
#     teacher : Teacher = Relationship(back_populates="attendances")
#     status : str

# Fee Plan
# class FeePlan(SQLModel, table=True):
#     id : uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
#     # school_id : uuid.UUID = Field(default=None, foreign_key="school.id")
#     # school : School = Relationship(back_populates="feeplans", cascade_delete=True)
#     classsection : ClassSection = Relationship(back_populates="feeplan", cascade_delete=True)
#     fee : float
#     alert_date : datetime
#     # end_date : datetime
    
#     feerecords : list["FeeRecord"] = Relationship(back_populates="feeplan")

# Fee Record
# class FeeRecord(SQLModel, table=True):
#     id : uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
#     school : School = Relationship(back_populates="feerecords", cascade_delete=True)
#     feeplan : FeePlan = Relationship(back_populates="feerecords", cascade_delete=True)
#     student : Student = Relationship(back_populates="feerecords")
#     paid : bool
#     date_of_payment : datetime
    
    

