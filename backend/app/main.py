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
    allow_origins=["http://localhost:3000"],
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
    
    
    user = crud.get_user_by_id(engine = db, user_id=decoded_token["data"]["uid"], role=decoded_token["data"]["role"])
    
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

# Create an Admin user
@app.post("/api/admin", response_model=models.Admin) # response_model tells the output schema
async def createAdminUser(admin: models.Admin, current_user: Annotated[models.Admin, Depends(get_current_user)], db: Session = Depends(get_session)):
    
    if current_user["role"] == "admin":
        try:
            password = random_password_generator()
            db_user = crud.createAdminUser(db, admin, hash_password(password))
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
        
        # print("admin schema: ", admin)
        if admin.password != "":
            admin.password = hash_password(admin.password)
        try:
            updated_user = crud.updateAdminUser(engine=db, admin=admin)
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
                teacher_users = crud.getTeacherUser(engine=db, id=id, name=name, email=email, phone=phone, school=crud.get_user_by_id(db, school_id, "school")["user"])
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
        # print("Current User id: ", current_user['user'])
        # print("school: ", school)
        try:
            password = random_password_generator()
            
            if current_user['role'] == 'school':
                db_user = crud.createStudentUser(db, current_user['user'], student, hash_password(password))
            else:
                db_user = crud.createStudentUser(db, crud.get_user_by_id(db, str(student.school_id), "school")['user'], student, hash_password(password))
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
                teacher_users = crud.getStudentUser(engine=db, id=id, name=name, email=email, phone=phone, school=crud.get_user_by_id(db, school_id, "school")["user"])
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

# Delete ClassSection - skipped in MVP
@app.delete("/api/classsection", response_model=models.Student)
async def deleteClassSection(student: models.Student, current_user: Annotated[models.Admin, Depends(get_current_user)], db: Session = Depends(get_session)):
    if current_user["role"] in ["admin","school"]:
        try:
            deleted_user = crud.deleteStudentUser(engine=db, student=student)
            print("deleted_user: ", deleted_user)
            return JSONResponse(content={"message":"User deletion successful!", "data": deleted_user}, status_code=status.HTTP_200_OK)
        except Exception as e:
            return JSONResponse(content={"message":f"Error: {e}"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    return JSONResponse(content={"message":"You are not authorized for this action."}, status_code=status.HTTP_401_UNAUTHORIZED)
# End ClassSection





if __name__ == "__main__":
    print(get_session())
