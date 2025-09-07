from sqlmodel import select, Session
from . import models, schema
import uuid


roles = {
    "admin":models.Admin,
    "school":models.School,
    "teacher":models.Teacher,
    "student":models.Student
}

def determine_usermodel(role: str):
    if role.lower() in roles.keys():
        usermodel = roles[role.lower()]
        return usermodel
    return None

def getUserByEmail(engine, user : schema.LoginUser):
    
    usermodel = determine_usermodel(user.role)
    if usermodel:
        # print("usermodel: ", usermodel, type(usermodel))
        statement = select(usermodel).where(usermodel.email==user.email)
        user = engine.exec(statement = statement).first() # engine is already a session, so we don't need to do Session(engine)
        return user
    return None

# from uuid import UUID
def get_user_by_id(engine: Session, user_id, role):
    
    usermodel = determine_usermodel(role)
    if usermodel:
        statement = select(usermodel).where(usermodel.id==uuid.UUID(user_id))
        return { "user": engine.exec(statement = statement).first(), "role":role.lower()}
    return None

# Create User
def createAdminUser(engine: Session, adminuser: models.Admin, password: str):
    db_user = models.Admin(
        name = adminuser.name,
        password = password,
        email= adminuser.email,
        phone= adminuser.phone
    )
    
    engine.add(db_user)
    engine.commit()
    engine.refresh(db_user)
    return db_user
    
    

    


    