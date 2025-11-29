from sqlmodel import Field, SQLModel, Relationship
from pydantic import EmailStr
from datetime import date, datetime

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

    students: list["Student"] = Relationship(back_populates="school", cascade_delete=True)
    teachers: list["Teacher"] = Relationship(back_populates="school", cascade_delete=True)
    
    created_by : Admin = Relationship(back_populates="schools")
    admin_id: uuid.UUID = Field(default=None, foreign_key="admin.id", ondelete="CASCADE") # To delete related school records, if someone delete admin from DB directly.
    
    classes: list["ClassSection"] = Relationship(back_populates="school", cascade_delete=True)
    # feeplans : list["FeePlan"] = Relationship(back_populates="school")
    
    
    

# Teacher SET NULL on attendance list
# Teacher User model
class Teacher(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    email: EmailStr = Field(nullable=False, unique=True, primary_key=True)
    phone: str = Field(max_length=15)
    password: str

    school_id: uuid.UUID = Field(default=None, foreign_key="school.id", ondelete="CASCADE")
    school: School = Relationship(back_populates="teachers")
    
    classsection : list["ClassSection"] = Relationship(back_populates="classteacher")
    attendances : list["Attendance"] = Relationship(back_populates="teacher")
    
    

# Student User Model
class Student(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    email: EmailStr = Field(nullable=False, unique=True)
    phone: str = Field(max_length=15)
    password: str

    school_id: uuid.UUID = Field(default=None, foreign_key="school.id", ondelete="CASCADE")
    school: School = Relationship(back_populates="students")
    
    
    classsection_id: uuid.UUID | None = Field(default=None, foreign_key="classsection.id", ondelete="SET NULL")
    classsection : "ClassSection" = Relationship(back_populates="students", passive_deletes=True)
    
    attendances : list["Attendance"] = Relationship(back_populates="student")
    feerecords : list["FeeRecord"] = Relationship(back_populates="student")


# Class model
class ClassSection(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    
    school_id: uuid.UUID = Field(default=None, foreign_key="school.id", ondelete="CASCADE")
    school: School = Relationship(back_populates="classes")
    
    classname: str
    
    classteacher_id: uuid.UUID | None = Field(default=None, foreign_key="teacher.id", ondelete="SET NULL")
    classteacher : Teacher = Relationship(back_populates="classsection")
    
    feeplan : "FeePlan" = Relationship(back_populates="classsection")
    # feerecords: list["FeeRecord"] = Relationship(back_populates="classsection")
    
    students : list["Student"] = Relationship(back_populates="classsection", passive_deletes=True)
    attendances : list["Attendance"] = Relationship(back_populates="classsection", passive_deletes=True)

# Attendance Record
class Attendance(SQLModel, table=True):
    id : uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    
    attendance_date : date
    attendance_status : str # Present/Absent/Leave/Late etc.
    
    # Foreign Keys (nullable, because teacher/student/class may be deleted)
    student_id: uuid.UUID | None = Field(foreign_key="student.id", ondelete="SET NULL")
    classsection_id: uuid.UUID | None = Field(foreign_key="classsection.id", ondelete="SET NULL")
    teacher_id: uuid.UUID | None = Field(foreign_key="teacher.id", ondelete="SET NULL")

    # Snapshot fields
    student_name: str
    class_name: str
    teacher_name: str
    
    student : "Student" = Relationship(back_populates="attendances")
    teacher : "Teacher" = Relationship(back_populates="attendances")
    classsection : "ClassSection" = Relationship(back_populates="attendances")
    
    
    

# Fee Plan
class FeePlan(SQLModel, table=True):
    id : uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    
    # class section
    classsection_id: uuid.UUID | None = Field(foreign_key="classsection.id", ondelete="SET NULL")
    classsection: "ClassSection" = Relationship(back_populates="feeplan")
    
    # Class name
    class_name: str
    
    # Fee Records
    feerecords: list["FeeRecord"] = Relationship(back_populates="feeplan")
    
    # Fee amount
    fee : float
    
    # Alert month-year
    alert_date: date
    
    
    

# Fee Record
class FeeRecord(SQLModel, table=True):
    id : uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
        
    # Student
    student_id: uuid.UUID | None = Field(foreign_key="student.id", ondelete="SET NULL")
    student : "Student" = Relationship(back_populates="feerecords")
    student_name: str
    
    # fee plan
    feeplan_id: uuid.UUID | None = Field(foreign_key="feeplan.id", ondelete="SET NULL")
    feeplan: "FeePlan" = Relationship(back_populates="feerecords")
    
    paid : bool
    
    payment_timestamp : datetime
    
    

