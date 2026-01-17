from fastapi import FastAPI, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from sqlmodel import SQLModel, Session
from . import models, crud

from .database import engine
SQLModel.metadata.create_all(engine)

from typing import Annotated, Optional

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_session():
    with Session(engine) as session:
        yield session
   
    
from fastapi.security import OAuth2PasswordBearer
from .security.token import encoding, decoding

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_session)):
    # print("token: ", token)
    decoded_token = decoding(token)
    # print(type(decoded_token["data"]))
    # print("Decoded token: ", decoded_token)
    print("decoded_token: ", decoded_token)
    
    
    user = crud.get_user_by_id(engine = db, user_id=decoded_token["data"]["uid"], role=decoded_token["data"]["role"])
    
    print("user: ", user)
    if user == None:
        raise Exception(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    return user


@app.get("/")
async def root():
	return {"message":"Hello, World!"}

@app.get("/test")
async def test(current_user: Annotated[models.Admin, Depends(get_current_user)], db: Session = Depends(get_session)):
    print("current user is: ",current_user)
    return {"message":"Hello, World!"}

@app.post("/profile")
async def profile(current_user: Annotated[models.Admin, Depends(get_current_user)], db: Session = Depends(get_session)):
    user = current_user["user"]
    role = current_user["role"]
    user_dict = {
        "userid": str(user.id),
        "username": user.name,
        "phone": user.phone,
        "email": user.email,
        "role": role
    }
    return JSONResponse(content={"message": "Profile fetch successful!", "data": user_dict }, status_code=status.HTTP_200_OK)
    

from .security.passwordhashing import hash_password

from . import schema


# User Login
@app.post("/api/login")
async def loginAdminUser(user: schema.LoginUser, db: Session = Depends(get_session)):
    
    db_user = crud.getUserByEmail(db, user)
    if db_user:
        # Now check the passwords!
        if hash_password(user.password) == db_user.password:
            jwt_token = encoding(db_user.id, user.role.lower())
            return JSONResponse(content={"message": "Login successful!", "token": jwt_token }, status_code=status.HTTP_200_OK)
        else:
            return JSONResponse(content={"message":"Incorrect Password!"}, status_code=status.HTTP_401_UNAUTHORIZED)
    
    return JSONResponse(content={"message":"User not found!"}, status_code=status.HTTP_404_NOT_FOUND)


# USER MANAGEMENT CODE
# Admin Users
# Create Admin User
from .security.passwordhashing import random_password_generator
from .MailHandler.mailer import send_email, EmailSubject, EmailType
# Create an Admin user
@app.post("/api/admin", response_model=models.Admin) # response_model tells the output schema
async def createAdminUser(admin: models.Admin, current_user: Annotated[models.Admin, Depends(get_current_user)], db: Session = Depends(get_session)):
    
    if current_user["role"] == "admin":
        try:
            password = random_password_generator()
            db_user = crud.createAdminUser(db, admin, hash_password(password))
            if db_user:
                # Now send password to user
                send_email(
                email_type=EmailType.NEW_USER_REGISTRATION,
                subject=EmailSubject['NEW_USER_REGISTRATION'],
                message_variables={
                    "username": db_user.name,
                    "password": password,
                    "role": "Admin"
                },
                recipient_email=db_user.email,
            )
                print("Will test email sending", password)
                pass
            
            return JSONResponse(content={"message":"User created Successfully!", "uid": str(db_user.id)}, status_code=status.HTTP_201_CREATED)
        except Exception as e:
            if "Duplicate entry" in str(e):
                e = "Email Already Exists!"
            return JSONResponse(content={"message":f"Error: {e}"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    return JSONResponse(content={"message":"You are not authorized for this action."}, status_code=status.HTTP_401_UNAUTHORIZED)


from pydantic import EmailStr

# Read Admin Users as per the filter
@app.get("/api/admin", response_model=list[models.Admin])
async def getAdminUser(
    current_user: Annotated[models.Admin, Depends(get_current_user)], 
    id: str = "*", 
    name: str = "*", 
    email: Optional[str] = "*", 
    phone : str="*",  
    db: Session = Depends(get_session)):
    
    if current_user["role"] == "admin":
        if id=="*":
            id=""
        if name=="*":
            name=""
        if email=="*":
            email=""
        if phone=="*":
            phone=""
        
        try:
            admin_users = crud.getAdminUser(engine=db, id=id, name=name, email=email, phone=phone)
            return JSONResponse(content={"message":"Operation Successful", "data": admin_users}, status_code=status.HTTP_200_OK)
        
        except Exception as e:
             return JSONResponse(content={"message":f"Error: {e}"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    return JSONResponse(content={"message":"You are not authorized for this action."}, status_code=status.HTTP_401_UNAUTHORIZED)

# Update Admin user
@app.put("/api/admin", response_model=models.Admin)
async def updateAdminUser(admin: models.Admin, current_user: Annotated[models.Admin, Depends(get_current_user)], db: Session = Depends(get_session)):
    if current_user["role"] == "admin":
        new_password = admin.password
        
        # print("admin schema: ", admin)
        if admin.password != "":
            admin.password = hash_password(admin.password)
        try:
            updated_user = crud.updateAdminUser(engine=db, admin=admin)
            
            if updated_user:
                # Now send password reset mail to the user
                send_email(
                    email_type=EmailType.PASSWORD_RESET,
                    subject=EmailSubject['PASSWORD_RESET'],
                    message_variables={
                        "username":updated_user['name'],
                        "password": new_password
                    },
                    recipient_email=updated_user['email']
                )
            print("updated_user: ", updated_user)
            return JSONResponse(content={"message":"User update successful!", "data": updated_user}, status_code=status.HTTP_200_OK)
        except Exception as e:
            return JSONResponse(content={"message":f"Error: {e}"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    return JSONResponse(content={"message":"You are not authorized for this action."}, status_code=status.HTTP_401_UNAUTHORIZED)
        

# Delete Admin user
@app.delete("/api/admin", response_model=models.Admin)
async def deleteAdminUser(admin: models.Admin, current_user: Annotated[models.Admin, Depends(get_current_user)], db: Session = Depends(get_session)):
    if current_user["role"] == "admin":
        try:
            deleted_user = crud.deleteAdminUser(engine=db, admin=admin)
            print("updated_user: ", deleted_user)
            return JSONResponse(content={"message":"User deletion successful!", "data": deleted_user}, status_code=status.HTTP_200_OK)
        except Exception as e:
            return JSONResponse(content={"message":f"Error: {e}"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    return JSONResponse(content={"message":"You are not authorized for this action."}, status_code=status.HTTP_401_UNAUTHORIZED)
# End Admin Users

# School Users
# Create a School user
@app.post("/api/school", response_model=models.School) # response_model tells the output schema
async def createSchoolUser(school: models.School, current_user: Annotated[models.Admin, Depends(get_current_user)], db: Session = Depends(get_session)):
    
    if current_user["role"] == "admin":
        # print("Current User id: ", current_user['user'])
        # print("school: ", school)
        try:
            password = random_password_generator()
            db_user = crud.createSchoolUser(db, current_user['user'], school, hash_password(password))
            return JSONResponse(content={"message":"User created Successfully!", "uid": str(db_user.id)}, status_code=status.HTTP_201_CREATED)
        except Exception as e:
            if "Duplicate entry" in str(e):
                e = "Email Already Exists!"
            return JSONResponse(content={"message":f"Error: {e}"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    return JSONResponse(content={"message":"You are not authorized for this action."}, status_code=status.HTTP_401_UNAUTHORIZED)

# Read School Users as per the filter
@app.get("/api/school", response_model=list[models.School])
async def getSchoolUser(
    current_user: Annotated[models.School, Depends(get_current_user)], 
    id: str = "*", 
    name: str = "*", 
    email: Optional[str] = "*", 
    phone : str="*",  
    db: Session = Depends(get_session)):
    
    if current_user["role"] == "admin":
        if id=="*":
            id=""
        if name=="*":
            name=""
        if email=="*":
            email=""
        if phone=="*":
            phone=""
        
        try:
            school_users = crud.getSchoolUser(engine=db, id=id, name=name, email=email, phone=phone)
            return JSONResponse(content={"message":"Operation Successful", "data": school_users}, status_code=status.HTTP_200_OK)
        
        except Exception as e:
             return JSONResponse(content={"message":f"Error: {e}"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    return JSONResponse(content={"message":"You are not authorized for this action."}, status_code=status.HTTP_401_UNAUTHORIZED)


# Update School user
@app.put("/api/school", response_model=models.School)
async def updateSchoolUser(school: models.School, current_user: Annotated[models.Admin, Depends(get_current_user)], db: Session = Depends(get_session)):
    if current_user["role"] == "admin":
        
        # print("admin schema: ", admin)
        if school.password != "":
            school.password = hash_password(school.password)
        try:
            updated_user = crud.updateSchoolUser(engine=db, school=school)
            print("updated_user: ", updated_user)
            return JSONResponse(content={"message":"User update successful!", "data": updated_user}, status_code=status.HTTP_200_OK)
        except Exception as e:
            return JSONResponse(content={"message":f"Error: {e}"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    return JSONResponse(content={"message":"You are not authorized for this action."}, status_code=status.HTTP_401_UNAUTHORIZED)
        
# Delete School user
@app.delete("/api/school", response_model=models.School)
async def deleteSchoolUser(school: models.School, current_user: Annotated[models.Admin, Depends(get_current_user)], db: Session = Depends(get_session)):
    if current_user["role"] == "admin":
        try:
            deleted_user = crud.deleteSchoolUser(engine=db, school=school)
            print("deleted_user: ", deleted_user)
            return JSONResponse(content={"message":"User deletion successful!", "data": deleted_user}, status_code=status.HTTP_200_OK)
        except Exception as e:
            return JSONResponse(content={"message":f"Error: {e}"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    return JSONResponse(content={"message":"You are not authorized for this action."}, status_code=status.HTTP_401_UNAUTHORIZED)
# End School Users

# Teacher User
# Create a Teacher user
@app.post("/api/teacher", response_model=models.Teacher) # response_model tells the output schema
async def createTeacherUser(teacher: models.Teacher, current_user: Annotated[models.Admin, Depends(get_current_user)], db: Session = Depends(get_session)):
    
    if current_user["role"] in ["admin","school"]:
        # print("Current User id: ", current_user['user'])
        # print("school: ", school)
        try:
            password = random_password_generator()
            
            if current_user['role'] == 'school':
                db_user = crud.createTeacherUser(db, current_user['user'], teacher, hash_password(password))
            else:
                db_user = crud.createTeacherUser(db, crud.get_user_by_id(db, str(teacher.school_id), "school")['user'], teacher, hash_password(password))
            return JSONResponse(content={"message":"User created Successfully!", "uid": str(db_user.id)}, status_code=status.HTTP_201_CREATED)
        except Exception as e:
            if "Duplicate entry" in str(e):
                e = "Email Already Exists!"
            return JSONResponse(content={"message":f"Error: {e}"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    return JSONResponse(content={"message":"You are not authorized for this action."}, status_code=status.HTTP_401_UNAUTHORIZED)


# Read Teacher Users as per the filter
@app.get("/api/teacher", response_model=list[models.Teacher])
async def getTeacherUser(
    current_user: Annotated[models.Admin, Depends(get_current_user)], 
    id: str = "*", 
    name: str = "*", 
    email: Optional[str] = "*", 
    phone : str="*",  
    school_id: str="*",
    db: Session = Depends(get_session)):
    
    if current_user["role"] in ["admin", "school"]:
        if id=="*":
            id=""
        if name=="*":
            name=""
        if email=="*":
            email=""
        if phone=="*":
            phone=""
        
        try:
            
            if current_user['role'] == 'school':
                teacher_users = crud.getTeacherUser(engine=db, id=id, name=name, email=email, phone=phone, school=current_user["user"])
            else:
                teacher_users = crud.getTeacherByAdmin(engine=db, id=id, name=name, email=email, phone=phone)
            return JSONResponse(content={"message":"Operation Successful", "data": teacher_users}, status_code=status.HTTP_200_OK)
        
        except Exception as e:
             return JSONResponse(content={"message":f"Error: {e}"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    return JSONResponse(content={"message":"You are not authorized for this action."}, status_code=status.HTTP_401_UNAUTHORIZED)

# Update Teacher user
@app.put("/api/teacher", response_model=models.Teacher)
async def updateTeacherUser(teacher: models.Teacher, current_user: Annotated[models.Admin, Depends(get_current_user)], db: Session = Depends(get_session)):
    if current_user["role"] in ["admin", "school"]:
        
        # print("admin schema: ", admin)
        if teacher.password != "":
            teacher.password = hash_password(teacher.password)
        try:
            updated_user = crud.updateTeacherUser(engine=db, teacher=teacher)
            print("updated_user: ", updated_user)
            return JSONResponse(content={"message":"Teacher update successful!", "data": updated_user}, status_code=status.HTTP_200_OK)
        except Exception as e:
            return JSONResponse(content={"message":f"Error: {e}"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    return JSONResponse(content={"message":"You are not authorized for this action."}, status_code=status.HTTP_401_UNAUTHORIZED)

# Delete Teacher user
@app.delete("/api/teacher", response_model=models.Teacher)
async def deleteTeacherUser(teacher: models.Teacher, current_user: Annotated[models.Admin, Depends(get_current_user)], db: Session = Depends(get_session)):
    if current_user["role"] in ["admin","school"]:
        try:
            deleted_user = crud.deleteTeacherUser(engine=db, teacher=teacher)
            print("deleted_user: ", deleted_user)
            return JSONResponse(content={"message":"User deletion successful!", "data": deleted_user}, status_code=status.HTTP_200_OK)
        except Exception as e:
            return JSONResponse(content={"message":f"Error: {e}"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    return JSONResponse(content={"message":"You are not authorized for this action."}, status_code=status.HTTP_401_UNAUTHORIZED)

# End Teacher Users


# Student User
# Create a Student user
@app.post("/api/student", response_model=models.Student) # response_model tells the output schema
async def createStudentUser(student: models.Student, current_user: Annotated[models.Admin, Depends(get_current_user)], db: Session = Depends(get_session)):
    
    
    
    if current_user["role"] in ["admin","school"]:
        
        try:
            password = random_password_generator()
            
            if current_user['role'] == 'school':
                # WORKING HERE
                db_user = crud.createStudentUser(db, current_user['user'], student, hash_password(password), classsection=crud.get_items_by_id(db, item_id=student.classsection_id, item_type="classsection"))
            else:
                db_user = crud.createStudentUser(db, crud.get_user_by_id(db, str(student.school_id), "school")['user'], student, hash_password(password), classsection=crud.get_items_by_id(db, item_id=student.classsection_id, item_type="classsection"))
                
            return JSONResponse(content={"message":"User created Successfully!", "uid": str(db_user.id)}, status_code=status.HTTP_201_CREATED)
        except Exception as e:
            if "Duplicate entry" in str(e):
                e = "Email Already Exists!"
            return JSONResponse(content={"message":f"Error: {e}"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    return JSONResponse(content={"message":"You are not authorized for this action."}, status_code=status.HTTP_401_UNAUTHORIZED)


# Read Student Users as per the filter
@app.get("/api/student", response_model=list[models.Student])
async def getStudentUser(
    current_user: Annotated[models.Admin, Depends(get_current_user)], 
    id: str = "*", 
    name: str = "*", 
    email: Optional[str] = "*", 
    phone : str="*",  
    school_id: str="*",
    db: Session = Depends(get_session)):
    
    if current_user["role"] in ["admin", "school"]:
        if id=="*":
            id=""
        if name=="*":
            name=""
        if email=="*":
            email=""
        if phone=="*":
            phone=""
        
        try:
            
            if current_user['role'] == 'school':
                teacher_users = crud.getStudentUser(engine=db, id=id, name=name, email=email, phone=phone, school=current_user["user"])
            else:
                teacher_users = crud.getStudentByAdmin(engine=db, id=id, name=name, email=email, phone=phone)
            return JSONResponse(content={"message":"Operation Successful", "data": teacher_users}, status_code=status.HTTP_200_OK)
        
        except Exception as e:
             return JSONResponse(content={"message":f"Error: {e}"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    return JSONResponse(content={"message":"You are not authorized for this action."}, status_code=status.HTTP_401_UNAUTHORIZED)

# Update Student user
@app.put("/api/student", response_model=models.Student)
async def updateStudentUser(student: models.Student, current_user: Annotated[models.Admin, Depends(get_current_user)], db: Session = Depends(get_session)):
    if current_user["role"] in ["admin", "school"]:
        
        # print("admin schema: ", admin)
        if student.password != "":
            student.password = hash_password(student.password)
        try:
            updated_user = crud.updateStudentUser(engine=db, student=student)
            print("updated_user: ", updated_user)
            return JSONResponse(content={"message":"Student update successful!", "data": updated_user}, status_code=status.HTTP_200_OK)
        except Exception as e:
            return JSONResponse(content={"message":f"Error: {e}"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    return JSONResponse(content={"message":"You are not authorized for this action."}, status_code=status.HTTP_401_UNAUTHORIZED)

# Delete Student user
@app.delete("/api/student", response_model=models.Student)
async def deleteStudentUser(student: models.Student, current_user: Annotated[models.Admin, Depends(get_current_user)], db: Session = Depends(get_session)):
    if current_user["role"] in ["admin","school"]:
        try:
            deleted_user = crud.deleteStudentUser(engine=db, student=student)
            print("deleted_user: ", deleted_user)
            return JSONResponse(content={"message":"User deletion successful!", "data": deleted_user}, status_code=status.HTTP_200_OK)
        except Exception as e:
            return JSONResponse(content={"message":f"Error: {e}"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    return JSONResponse(content={"message":"You are not authorized for this action."}, status_code=status.HTTP_401_UNAUTHORIZED)

# End Student Users




# ClassSection
# Create a ClassSection
@app.post("/api/classsection", response_model=models.ClassSection) # response_model tells the output schema
async def createClassSection(classsection: models.ClassSection, current_user: Annotated[models.Admin, Depends(get_current_user)], db: Session = Depends(get_session)):
    
    if current_user["role"] in ["admin","school"]:
        try:
            # password = random_password_generator()
            
            if current_user['role'] == 'school':
                db_item = crud.createClassSection(db, classsection.classname, current_user['user'], crud.get_user_by_id(db, str(classsection.classteacher_id), "teacher")['user'])
            else:
                db_item = crud.createClassSection(db, classsection.classname, crud.get_user_by_id(db, str(classsection.school_id), "school")['user'], crud.get_user_by_id(db, str(classsection.classteacher_id), "teacher")['user'])
            return JSONResponse(content={"message":"ClassSection created Successfully!", "id": str(db_item.id)}, status_code=status.HTTP_201_CREATED)
        except Exception as e:
            if "Duplicate entry" in str(e):
                e = "Email Already Exists!"
            return JSONResponse(content={"message":f"Error: {e}"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    return JSONResponse(content={"message":"You are not authorized for this action."}, status_code=status.HTTP_401_UNAUTHORIZED)




# Read ClassSection as per the filter
@app.get("/api/classsection", response_model=list[models.ClassSection])
async def getClassSection(
    current_user: Annotated[models.Admin, Depends(get_current_user)], 
    id: str = "*", # record id
    school_id: str = "*",
    classteacher_id: str = "*",
    classname: str="*",
    db: Session = Depends(get_session)):
    
    if current_user["role"] in ["admin", "school"]:    
        try:
            
            if current_user['role'] != 'school':
                if school_id != "*":
                    school = crud.get_user_by_id(db, school_id, "school")['user']
                else:
                    school = models.School()
                    school.id = None
            else:
                school=current_user["user"]
                
            if classteacher_id != "*":
                teacher = crud.get_user_by_id(db, classteacher_id, "teacher")['user']
            else:
                teacher = models.Teacher()
                teacher.id = None    
                
            classsection_items = crud.getClassSection(engine=db, id=id, classname=classname, school=school, classteacher = teacher)
               
            return JSONResponse(content={"message":"Operation Successful", "data": classsection_items}, status_code=status.HTTP_200_OK)
        
        except Exception as e:
             return JSONResponse(content={"message":f"Error: {e}"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    return JSONResponse(content={"message":"You are not authorized for this action."}, status_code=status.HTTP_401_UNAUTHORIZED)

# Update ClassSection 
@app.put("/api/classsection", response_model=models.ClassSection)
async def updateClassSection(classsection: models.ClassSection, current_user: Annotated[models.Admin, Depends(get_current_user)], db: Session = Depends(get_session)):
    if current_user["role"] in ["admin", "school"]:
        
        
        try:
            classsection.school = crud.get_user_by_id(engine=db, user_id=classsection.school_id, role="school")["user"]
            classsection.classteacher = crud.get_user_by_id(engine=db, user_id=classsection.classteacher_id, role="teacher")["user"]
            updated_classsection = crud.updateClassSection(engine=db, classsection=classsection)
            print("updated_classsection: ", updated_classsection)
            return JSONResponse(content={"message":"ClassSection update successful!", "data": updated_classsection}, status_code=status.HTTP_200_OK)
        except Exception as e:
            return JSONResponse(content={"message":f"Error: {e}"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    return JSONResponse(content={"message":"You are not authorized for this action."}, status_code=status.HTTP_401_UNAUTHORIZED)

# Delete ClassSection
@app.delete("/api/classsection/{id}")
async def deleteClassSection(id: str, current_user: Annotated[models.Admin, Depends(get_current_user)], db: Session = Depends(get_session)):
    if current_user["role"] in ["admin","school"]:
        try:
            deleted_record = crud.deleteClassSection(engine=db, classsection_id=id)
            print("deleted_user: ", deleted_record)
            return JSONResponse(content={"message":"Record deletion successful!", "data": deleted_record}, status_code=status.HTTP_200_OK)
        except Exception as e:
            return JSONResponse(content={"message":f"Error: {e}"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    return JSONResponse(content={"message":"You are not authorized for this action."}, status_code=status.HTTP_401_UNAUTHORIZED)
# End ClassSection

# Attendance
# Create a Attendance
@app.post("/api/attendance", response_model=models.Attendance) # response_model tells the output schema
async def createAttendance(attendance: models.Attendance, current_user: Annotated[models.Admin, Depends(get_current_user)], db: Session = Depends(get_session)):
    
    if current_user["role"] in ["admin","school", "teacher"]:
        try:
            # password = random_password_generator()
            
            # if current_user['role'] == 'school':
            #     db_item = crud.createClassSection(db, classsection.classname, current_user['user'], crud.get_user_by_id(db, str(classsection.classteacher_id), "teacher")['user'])
            # else:
            #     db_item = crud.createClassSection(db, classsection.classname, crud.get_user_by_id(db, str(classsection.school_id), "school")['user'], crud.get_user_by_id(db, str(classsection.classteacher_id), "teacher")['user'])
            
            # Class Name
            classsection = crud.get_items_by_id(engine=db, item_id=attendance.classsection_id, item_type="classsection")
            attendance.class_name = classsection.classname
            
            # Student Name
            student = crud.get_user_by_id(engine=db, user_id=attendance.student_id, role="student")["user"]
            attendance.student_name = student.name
            
            # Teacher Name
            teacher = crud.get_user_by_id(engine=db, user_id=attendance.teacher_id, role="teacher")["user"]
            attendance.teacher_name = teacher.name
            
            # School
            school = crud.get_user_by_id(engine=db, user_id=attendance.school_id, role="school")["user"]
            attendance.school = school
            
            db_item = crud.createAttendance(db, attendance = attendance)
            return JSONResponse(content={"message":"Attendance created Successfully!", "id": str(db_item.id)}, status_code=status.HTTP_201_CREATED)
        except Exception as e:
            if "Duplicate entry" in str(e):
                e = "Duplication occurred!"
            return JSONResponse(content={"message":f"Error: {e}"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    return JSONResponse(content={"message":"You are not authorized for this action."}, status_code=status.HTTP_401_UNAUTHORIZED)




# Read Attendance as per the filter
@app.get("/api/attendance", response_model=list[models.Attendance])
async def getAttendance(
    current_user: Annotated[models.Admin, Depends(get_current_user)], 
    school_id: str,
    id: str = "*", # record id
    attendance_status: str="*",
    student_name: str = "*",
    class_name: str="*",
    teacher_name: str="*",
    attendance_date: str="*",
    db: Session = Depends(get_session)):
    
    if current_user["role"] in ["admin", "school", "teacher"]:    
        try:
            
            school = crud.get_user_by_id(engine=db, user_id=school_id, role="school")["user"]
            
            print("school is: ", school)
            attendance_items = crud.getAttendance(engine=db, id=id, attendance_status=attendance_status, attendance_date=attendance_date, student_name=student_name, class_name=class_name, teacher_name=teacher_name, school=school)
               
            return JSONResponse(content={"message":"Operation Successful", "data": attendance_items}, status_code=status.HTTP_200_OK)
        
        except Exception as e:
             return JSONResponse(content={"message":f"Error: {e}"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    return JSONResponse(content={"message":"You are not authorized for this action."}, status_code=status.HTTP_401_UNAUTHORIZED)

# Update Attendance 
@app.put("/api/attendance", response_model=models.Attendance)
async def updateAttendance(attendance: models.Attendance, current_user: Annotated[models.Admin, Depends(get_current_user)], db: Session = Depends(get_session)):
    if current_user["role"] in ["admin", "school", "teacher"]:
        try:
            updated_attendance = crud.updateAttendance(engine=db, attendance=attendance)
            
            print("updated_attendance: ", updated_attendance)
            
            return JSONResponse(content={"message":"Attendance update successful!", "data": updated_attendance}, status_code=status.HTTP_200_OK)
        
        except Exception as e:
            return JSONResponse(content={"message":f"Error: {e}"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    return JSONResponse(content={"message":"You are not authorized for this action."}, status_code=status.HTTP_401_UNAUTHORIZED)

# Delete Attendance
@app.delete("/api/attendance/{id}")
async def deleteAttendance(id: str, current_user: Annotated[models.Admin, Depends(get_current_user)], db: Session = Depends(get_session)):
    if current_user["role"] in ["admin","school", "teacher"]:
        try:
            deleted_record = crud.deleteAttendance(engine=db, id=id)
            print("deleted_attendance: ", deleted_record)
            return JSONResponse(content={"message":"Record deletion successful!", "data": deleted_record}, status_code=status.HTTP_200_OK)
        except Exception as e:
            return JSONResponse(content={"message":f"Error: {e}"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    return JSONResponse(content={"message":"You are not authorized for this action."}, status_code=status.HTTP_401_UNAUTHORIZED)
# End Attendance

# Fee Plan
# Create a Fee Plan
@app.post("/api/fee/plan", response_model=models.FeePlan) # response_model tells the output schema
async def createFeePlan(feeplan: models.FeePlan, current_user: Annotated[models.Admin, Depends(get_current_user)], db: Session = Depends(get_session)):
    
    if current_user["role"] in ["admin","school"]:
        try:
            # School
            school = crud.get_user_by_id(engine=db, user_id=feeplan.school_id, role="school")["user"]
            feeplan.school = school
            
            db_item = crud.createFeePlan(db, feeplan = feeplan)
            return JSONResponse(content={"message":"Fee Plan created Successfully!", "id": str(db_item.id)}, status_code=status.HTTP_201_CREATED)
        except Exception as e:
            if "Duplicate entry" in str(e):
                e = "Duplication occurred!"
            return JSONResponse(content={"message":f"Error: {e}"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    return JSONResponse(content={"message":"You are not authorized for this action."}, status_code=status.HTTP_401_UNAUTHORIZED)




# Read Attendance as per the filter
@app.get("/api/fee/plan", response_model=list[models.FeePlan])
async def getFeePlan(
    current_user: Annotated[models.Admin, Depends(get_current_user)], 
    school_id: str,
    
    
    id: str = "*", # record id

    classsection_id: str="*",
    class_name: str="*",
    
    fee: str="*",
    alert_date: str="*",
    db: Session = Depends(get_session)):
    
    if current_user["role"] in ["admin", "school"]:    
        try:
            
            school = crud.get_user_by_id(engine=db, user_id=school_id, role="school")["user"]
            
            print("school is: ", school)
            
            # add specific to school also, otherwise other schools can see each other fee records
            feeplan_items = crud.getFeePlan(engine=db, id=id, classsection_id=classsection_id, class_name=class_name, fee=fee, alert_date=alert_date, school=school)
               
            return JSONResponse(content={"message":"Operation Successful", "data": feeplan_items}, status_code=status.HTTP_200_OK)
        
        except Exception as e:
             return JSONResponse(content={"message":f"Error: {e}"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    return JSONResponse(content={"message":"You are not authorized for this action."}, status_code=status.HTTP_401_UNAUTHORIZED)

# Update FeePlan 
@app.put("/api/fee/plan", response_model=models.FeePlan)
async def updateFeePlan(feeplan: models.FeePlan, current_user: Annotated[models.Admin, Depends(get_current_user)], db: Session = Depends(get_session)):
    if current_user["role"] in ["admin", "school"]:
        try:
            updated_feeplan = crud.updateFeePlan(engine=db, feeplan=feeplan)
            
            print("updated_feeplan: ", updated_feeplan)
            
            return JSONResponse(content={"message":"Fee Plan update successful!", "data": updated_feeplan}, status_code=status.HTTP_200_OK)
        
        except Exception as e:
            return JSONResponse(content={"message":f"Error: {e}"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    return JSONResponse(content={"message":"You are not authorized for this action."}, status_code=status.HTTP_401_UNAUTHORIZED)

# Delete FeePlan
@app.delete("/api/fee/plan/{id}")
async def deleteFeePlan(id: str, current_user: Annotated[models.Admin, Depends(get_current_user)], db: Session = Depends(get_session)):
    if current_user["role"] in ["admin","school"]:
        try:
            deleted_record = crud.deleteFeePlan(engine=db, id=id)
            print("deleted_feeplan: ", deleted_record)
            return JSONResponse(content={"message":"Record deletion successful!", "data": deleted_record}, status_code=status.HTTP_200_OK)
        except Exception as e:
            return JSONResponse(content={"message":f"Error: {e}"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    return JSONResponse(content={"message":"You are not authorized for this action."}, status_code=status.HTTP_401_UNAUTHORIZED)
# End FeePlan

# Fee 
# Create a Fee Record
@app.post("/api/fee", response_model=models.FeeRecord) # response_model tells the output schema
async def createFeeRecord(feerecord: models.FeeRecord, current_user: Annotated[models.Admin, Depends(get_current_user)], db: Session = Depends(get_session)):
    
    if current_user["role"] in ["admin", "school", "student"]:
        try:
            # School
            school = crud.get_user_by_id(engine=db, user_id=feerecord.school_id, role="school")["user"]
            feerecord.school = school
            
            db_item = crud.createFeeRecord(db, feerecord = feerecord)
            return JSONResponse(content={"message":"Fee Record created Successfully!", "id": str(db_item.id)}, status_code=status.HTTP_201_CREATED)
        except Exception as e:
            if "Duplicate entry" in str(e):
                e = "Duplication occurred!"
            return JSONResponse(content={"message":f"Error: {e}"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    return JSONResponse(content={"message":"You are not authorized for this action."}, status_code=status.HTTP_401_UNAUTHORIZED)




# Read FeeRecord as per the filter
@app.get("/api/fee", response_model=list[models.FeeRecord])
async def getFeeRecord(
    current_user: Annotated[models.Admin, Depends(get_current_user)], 
    
    school_id: str,
    paid: bool,
    
    id: str = "*", # record id

    student_id: str="*",
    student_name: str="*",
    
    feeplan_id: str="*",
    payment_timestamp: str="*",
    db: Session = Depends(get_session)):
    
    if current_user["role"] in ["admin", "school"]:    
        try:
            
            school = crud.get_user_by_id(engine=db, user_id=school_id, role="school")["user"]
            
            print("school is: ", school)
            
            # add specific to school also, otherwise other schools can see each other fee records
            feeplan_items = crud.getFeeRecord(engine=db, id=id, student_id=student_id, student_name=student_name, feeplan_id=feeplan_id, paid=paid, payment_timestamp=payment_timestamp, school=school)
               
            return JSONResponse(content={"message":"Operation Successful", "data": feeplan_items}, status_code=status.HTTP_200_OK)
        
        except Exception as e:
             return JSONResponse(content={"message":f"Error: {e}"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    return JSONResponse(content={"message":"You are not authorized for this action."}, status_code=status.HTTP_401_UNAUTHORIZED)

# Update FeePlan 
@app.put("/api/fee", response_model=models.FeeRecord)
async def updateFeeRecord(feerecord: models.FeeRecord, current_user: Annotated[models.Admin, Depends(get_current_user)], db: Session = Depends(get_session)):
    if current_user["role"] in ["admin", "school", "student"]:
        try:
            updated_feerecord = crud.updateFeeRecord(engine=db, feerecord=feerecord)
            
            print("updated_feeplan: ", updated_feerecord)
            
            return JSONResponse(content={"message":"Fee Record update successful!", "data": updated_feerecord}, status_code=status.HTTP_200_OK)
        
        except Exception as e:
            return JSONResponse(content={"message":f"Error: {e}"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    return JSONResponse(content={"message":"You are not authorized for this action."}, status_code=status.HTTP_401_UNAUTHORIZED)

# Delete FeePlan
@app.delete("/api/fee/{id}")
async def deleteFeeRecord(id: str, current_user: Annotated[models.Admin, Depends(get_current_user)], db: Session = Depends(get_session)):
    if current_user["role"] in ["admin","school"]:
        try:
            deleted_record = crud.deleteFeeRecord(engine=db, id=id)
            print("deleted_feerecord: ", deleted_record)
            return JSONResponse(content={"message":"Record deletion successful!", "data": deleted_record}, status_code=status.HTTP_200_OK)
        except Exception as e:
            return JSONResponse(content={"message":f"Error: {e}"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    return JSONResponse(content={"message":"You are not authorized for this action."}, status_code=status.HTTP_401_UNAUTHORIZED)
# End Fee





if __name__ == "__main__":
    print(get_session())
