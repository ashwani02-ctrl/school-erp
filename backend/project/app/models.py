from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, JSON
from sqlalchemy.sql import text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import enum
from .database import Base

# Defining the types of users
class AccountType(enum.Enum):
    ADMIN = "Admin"
    SCHOOL = "School"
    TEACHER = "Teacher"
    STUDENT = "Student"
    
# Defining account status
class Status(enum.Enum):
    ACTIVE = "Active"
    INACTIVE = "Inactive"
    SUSPENDED = "Suspended"
    
    
# Defining Status of Update Request
# class UpdateRequestStatus(enum.Enum):
#     PENDING = "Pending"
#     APPROVED = "Approved"
#     REJECTED = "Rejected"

class AdminUser(Base):
        __tablename__ = "GeneralUser"
        
        # User id
        uid = Column(UUID(as_uuid=False), primary_key=True, server_default=text("UUID()"))
        
        # Username - name of the user i.e. student's name, placement user name, university user name and admin name (admins)
        username = Column(String(50), nullable=False)
        
        # password
        password = Column(String(100), nullable=False)
        
        # email
        email = Column(String(100), unique=True, nullable=False)
        
        # Date of creation
        created_on = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
        
        # Updated by (UID)
        created_by = Column(String(100))
        
        # Updated by (UID)
        updated_by = Column(String(100))
        
        # status -> active, inactive and suspended (i.e. deleted)
        status = Column(Enum(Status, native_enum=False), nullable=False)
        
        # Last login   
        last_login = Column(DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
        
        
class SchoolUser(Base):
        __tablename__ = "GeneralUser"
        
        # User id
        uid = Column(UUID(as_uuid=False), primary_key=True, server_default=text("UUID()"))
        
        # Username - name of the user i.e. student's name, placement user name, university user name and admin name (admins)
        username = Column(String(50), nullable=False)
        
        # password
        password = Column(String(100), nullable=False)
        
        # email
        email = Column(String(100), unique=True, nullable=False)
        
        # Date of creation
        created_on = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
        
        # Updated by (UID)
        created_by = Column(String(100))
        
        # Updated by (UID)
        updated_by = Column(String(100))
        
        # Last login   
        last_login = Column(DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
        
                
class TeacherUser(Base):
        __tablename__ = "GeneralUser"
        
        # User id
        uid = Column(UUID(as_uuid=False), primary_key=True, server_default=text("UUID()"))
        
        # Username - name of the user i.e. student's name, placement user name, university user name and admin name (admins)
        username = Column(String(50), nullable=False)
        
        # password
        password = Column(String(100), nullable=False)
        
        # email
        email = Column(String(100), unique=True, nullable=False)
        
        # Date of creation
        created_on = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
        
        # Created by (UID)
        created_by = Column(String(100))
        
        # Updated by (UID)
        updated_by = Column(String(100))
        
        # Last login   
        last_login = Column(DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
        
        # School ID
        school_id = Column(String(100))
        
class StudentUser(Base):
        __tablename__ = "GeneralUser"
        
        # User id
        uid = Column(UUID(as_uuid=False), primary_key=True, server_default=text("UUID()"))
        
        # Username - name of the user i.e. student's name, placement user name, university user name and admin name (admins)
        username = Column(String(50), nullable=False)
        
        # password
        password = Column(String(100), nullable=False)
        
        # email
        email = Column(String(100), unique=True, nullable=False)
                
        # Date of creation
        created_on = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
        
        # Created by (UID)
        created_by = Column(String(100))
        
        # Updated by (UID)
        updated_by = Column(String(100))
        
        # Last login   
        last_login = Column(DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
        
        # School ID
        school_id = Column(String(100))
      
# from datetime import date  
# class Student(Base):
#     __tablename__ = "Student"
    
#     # Student id
#     student_id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("UUID()"))
    
#     # User id
#     user_id = Column(UUID(as_uuid=True), ForeignKey("GeneralUser.user_id"), nullable=False)
    
#     # Phone number
#     phone_number = Column(String(10), nullable=False)

#     # DOB
#     dob = Column(DateTime, nullable=False)
    
#     # Address
#     address = Column(String(100), nullable=False)
    
#     # Study Record
#     # study_record = Column(UUID(as_uuid=True), ForeignKey("StudyRecord.study_record_id"), nullable=False)
    

    
# class StudyRecord(Base):
#     __tablename__ = "StudyRecord"
    
#     # Study record id
#     study_record_id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("UUID()"))
    
#     # Student id
#     student_id = Column(UUID(as_uuid=True), ForeignKey("Student.student_id"), nullable=False)
    
#     # Programme ID
#     programme_id = Column(UUID, ForeignKey("Programme.programme_id"), nullable=False)
    
#     # Current semester
#     current_semester = Column(Integer, nullable=False)
    
#     # Current CGPA
#     current_cgpa = Column(String(10), nullable=False)

# class Programme(Base):
#     __tablename__ = "Programme"
    
#     # Programme Record ID
#     programme_id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("UUID()"))
    
#     # Programme code
#     programme_code = Column(String(50), primary_key=True, unique=True, nullable=False)
    
#     # Programme name
#     programme_name = Column(String(100), nullable=False)
    
#     # Programme description
#     programme_description = Column(String(500), nullable=False)
    
#     # no of semesters
#     no_of_semesters = Column(Integer, nullable=False)
    


    
# import uuid
# # Resumes Table
# class Resume(Base):
#     __tablename__ = "Resume"
    
#     # Resume id
#     resume_id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("UUID()"))
    
#     # Student id
#     student_id = Column(UUID(as_uuid=True), ForeignKey("Student.student_id"), nullable=False)
    
#     # Resume file path on server
#     resume_file_path = Column(String(100), nullable=False)
    
#     # Resume file name
#     resume_file_name = Column(String(100), nullable=False)
    
#     # Resume file size
#     resume_file_size = Column(Integer, nullable=False)
    
#     # Job Application id
#     # job_application_id = Column(UUID(as_uuid=True), ForeignKey("JobApplication.job_application_id"), nullable=False, default=uuid.UUID(""))
    
# # Job Application
# class JobApplication(Base):
#     __tablename__ = "JobApplication"
    
#     # Job application id
#     job_application_id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("UUID()"))
    
#     # Student id
#     student_id = Column(UUID(as_uuid=True), ForeignKey("Student.student_id"), nullable=False)
    
#     # Job id
#     job_id = Column(UUID(as_uuid=True), ForeignKey("Job.job_id"), nullable=False)
    
#     # Resume id
#     resume_id = Column(UUID(as_uuid=True), ForeignKey("Resume.resume_id"), nullable=False)
    
#     # Date of application
#     application_date_time = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    
#     # Status of application - in future

# # Job Posts
# class Job(Base):
#     __tablename__ = "Job"
    
#     # Job id
#     job_id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("UUID()"))
    
#     # Job title
#     title = Column(String(100), nullable=False)
    
#     # Job description
#     description = Column(String(500), nullable=False)
    
#     # Company ID
#     company_id = Column(UUID(as_uuid=True), ForeignKey("Company.company_id"), nullable=False)
    
#     # Skills required
#     skills_required = Column(String(100), nullable=False)
    
#     # who can apply?
#     who_can_apply = Column(String(500), nullable=False) # list of program ids, load via json.load
    
#     # Deadline 
#     deadline = Column(DateTime, nullable=False)


# class UpdateRequest(Base):
#     __tablename__ = "UpdateRequest"
    
#     # Update request id
#     update_request_id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("UUID()"))
    
#     # Student id
#     student_id = Column(UUID(as_uuid=True), ForeignKey("Student.student_id"), nullable=False)
    
#     # Updatation fields
#     update_fields = Column(JSON, nullable=False) # It will be json
    
#     # Update request description
#     update_request_description = Column(String(500), nullable=False)
    
#     # Status of the request
#     status = Column(Enum(UpdateRequestStatus, native_enum=False), nullable=False)
    
#     # Date of Request
#     date_of_request = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    
#     # Date of last update
#     date_of_last_update = Column(DateTime, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
        
# class OTP(Base):
#     __tablename__ = "OTP"
    
#     # OTP id
#     otp_id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("UUID()"))
    
#     # User id
#     user_id = Column(UUID(as_uuid=True), ForeignKey("GeneralUser.user_id"), nullable=False)
    
#     # OTP
#     otp = Column(String(10), nullable=False)
    
#     # Date of creation
#     date_of_creation = Column(DateTime, server_default=text("CURRENT_TIMESTAMP"))

# class Company(Base):
#     __tablename__ = "Company"
    
#     # Company id
#     company_id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("UUID()"))
    
#     # Company name
#     company_name = Column(String(100), nullable=False)
    
#     # Company description
#     description = Column(String(500), nullable=False)
    
#     # email
#     company_email = Column(String(100), unique=True, nullable=False)
    
#     # URL
#     url = Column(String(100), nullable=False)
    
#     # HR Info as json
#     hr_info = Column(String(500), nullable=False) # It will be json