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

# Get Admin User
def getAdminUser(engine: Session, id: str, name:str, email : str, phone:str):
    
    if len(id) != 32:
        statement = select(models.Admin).where(
                # defining filters
                models.Admin.name.like(f"%{name}%"), 
                models.Admin.email.like(f"%{email}%"), 
                models.Admin.phone.like(f"%{phone}%")
            )
    else:
        statement = select(models.Admin).where(
                models.Admin.id == uuid.UUID(id), # id must be fixed
                models.Admin.name.like(f"%{name}%"), 
                models.Admin.email.like(f"%{email}%"), 
                models.Admin.phone.like(f"%{phone}%")
            )
        

    results = engine.exec(statement)
    
    output_list = list()
    for result in results:
        
        output_list.append({
            "id" : str(result.id),
            "name":result.name,
            "email":result.email,
            "phone":result.phone,
        })
    return output_list
    

# Update Admin User
def updateAdminUser(engine: Session, admin: schema.UpdateAdmin):
    statement = select(models.Admin).where(models.Admin.id == uuid.UUID(admin.id))
    results = engine.exec(statement)
    admin_user = results.one()
    
    if admin.password != "":
        admin_user.password = admin.password
    
    admin_user.name = admin.name
    admin_user.email = admin.email
    admin_user.phone = admin.phone
    
    engine.add(admin_user)
    engine.commit()
    engine.refresh(admin_user)
    print("Updated Admin: ", admin_user)
    
    
    
    updated_user =  dict(admin_user)
    updated_user['id'] = str(updated_user['id'])
    return updated_user

# Delete Admin User
def deleteAdminUser(engine: Session, admin: schema.DeleteAdmin):
    statement = select(models.Admin).where(
        models.Admin.id == uuid.UUID(admin.id),
        models.Admin.name == admin.name,
        models.Admin.email  == admin.email,
        models.Admin.phone == admin.phone
        )
    results = engine.exec(statement)
    admin_user = results.one()
    
    print("selected admin_user: ", admin_user)
    engine.delete(admin_user)
    engine.commit()
    
    deleted_user =  dict(admin_user)
    deleted_user['id'] = str(deleted_user['id'])
    return deleted_user
    

# School User

# Create School User
def createSchoolUser(engine: Session, adminuser: models.Admin, schooluser: models.School, password: str):
    db_user = models.School(
        name = schooluser.name,
        password = password,
        email= schooluser.email,
        phone= schooluser.phone,
        created_by= adminuser,
        admin_id = adminuser.id
    )
    
    engine.add(db_user)
    engine.commit()
    engine.refresh(db_user)
    return db_user


from sqlalchemy.orm import selectinload
# Get School User
def getSchoolUser(engine: Session, id: str, name:str, email : str, phone:str):
    
    if len(id) != 32:
        statement = select(models.School).where(
                # defining filters
                models.School.name.like(f"%{name}%"), 
                models.School.email.like(f"%{email}%"), 
                models.School.phone.like(f"%{phone}%")
            ).options(selectinload(models.School.created_by))
        
    else:
        statement = select(models.School).where(
                models.School.id == uuid.UUID(id), # id must be fixed
                models.School.name.like(f"%{name}%"), 
                models.School.email.like(f"%{email}%"), 
                models.School.phone.like(f"%{phone}%")
            ).options(selectinload(models.School.created_by))
        
   
    results = engine.exec(statement)
    
    output_list = list()
    for result in results:    
        output_list.append({
            "id": str(result.id),
            "name":result.name,
            "email":result.email,
            "phone":result.phone,
            "created_by":{
                "id": str(result.created_by.id),
                "name":result.created_by.name,
                "email":result.created_by.email,
                "phone":result.created_by.phone,
            }
        })
   
    return output_list
    

# Update School User
def updateSchoolUser(engine: Session, school: models.School):
    statement = select(models.School).where(models.School.id == uuid.UUID(school.id))
    results = engine.exec(statement)
    school_user = results.one()
    
    if school.password != "":
        school_user.password = school.password
    
    school_user.name = school.name
    school_user.email = school.email
    school_user.phone = school.phone
    
    engine.add(school_user)
    engine.commit()
    engine.refresh(school_user)
    print("Updated School: ", school_user)
    
    
    
    updated_user =  dict(school_user)
    updated_user['id'] = str(updated_user['id'])
    updated_user['admin_id'] = str(updated_user['admin_id'])
    return updated_user
