from sqlmodel import select, Session
from . import models, schema
import uuid


# Mapping for item type
item_types = {
    "classsection": models.ClassSection,
}

# determine item model
def determine_itemmodel(item_type: str):
    if item_type.lower() in item_types.keys():
        item_model = item_types[item_type.lower()]
        return item_model
    return None

# Get things by id
def get_items_by_id(engine: Session, item_id, item_type):
    item_model = determine_itemmodel(item_type=item_type)
    if item_model:
        print("item_type: ", item_type)    
        print("item_id: ", item_id)
        statement = select(item_model).where(item_model.id==uuid.UUID(item_id))
        return engine.exec(statement).first()      
    print("Not worked for given item_type")
    return None

# Mapping of user roles
roles = {
    "admin":models.Admin,
    "school":models.School,
    "teacher":models.Teacher,
    "student":models.Student,
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
        print("statement: ", statement)
        return { "user": engine.exec(statement).first(), "role":role.lower()}      
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
    
    if len(id.replace("-", "")) != 32:
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
    updated_user.pop('password', None)
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
    deleted_user.pop('password', None)
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
    
    if len(id.replace("-","")) != 32:
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
    updated_user.pop('password', None)
    # updated_user.pop('created_by', None)
    updated_user['created_by'] = {
                "id": str(school_user.created_by.id),
                "name":school_user.created_by.name,
                "email":school_user.created_by.email,
                "phone":school_user.created_by.phone,
            }
    return updated_user


# Delete School User
def deleteSchoolUser(engine: Session, school: models.School):
    statement = select(models.School).where(
        models.School.id == uuid.UUID(school.id),
        models.School.name == school.name,
        models.School.email  == school.email,
        models.School.phone == school.phone
        )
    results = engine.exec(statement)
    school_user = results.one()
    
    print("selected school_user: ", school_user)
    engine.delete(school_user)
    engine.commit()
    
    deleted_user =  dict(school_user)
    deleted_user['id'] = str(deleted_user['id'])
    deleted_user['admin_id'] = str(deleted_user['admin_id'])
    deleted_user.pop('password', None)
    
    deleted_user['created_by'] = {
                "id": str(school_user.created_by.id),
                "name":school_user.created_by.name,
                "email":school_user.created_by.email,
                "phone":school_user.created_by.phone,
            }
    return deleted_user

# Create Teacher User
def createTeacherUser(engine: Session, schooluser: models.School, teacheruser: models.Teacher, password: str):
    db_user = models.Teacher(
        name = teacheruser.name,
        password = password,
        email= teacheruser.email,
        phone= teacheruser.phone,
        school= schooluser,
        school_id = schooluser.id
    )
    
    engine.add(db_user)
    engine.commit()
    engine.refresh(db_user)
    return db_user

# Get Teacher User
def getTeacherUser(engine: Session, id: str, name:str, email : str, phone:str, school: models.School):
    
   
    
    if len(id.replace("-","")) != 32:
        statement = select(models.Teacher).where(
                # defining filters
                models.Teacher.school_id == school.id,
                models.Teacher.name.like(f"%{name}%"), 
                models.Teacher.email.like(f"%{email}%"), 
                models.Teacher.phone.like(f"%{phone}%")
            ).options(selectinload(models.Teacher.school))
        
    else:
        statement = select(models.Teacher).where(
                models.Teacher.id == uuid.UUID(id), # id must be fixed
                models.Teacher.school_id == school.id,
                models.Teacher.name.like(f"%{name}%"), 
                models.Teacher.email.like(f"%{email}%"), 
                models.Teacher.phone.like(f"%{phone}%"),
            ).options(selectinload(models.Teacher.school))
    
    
   
    results = engine.exec(statement)
    
    output_list = list()
    for result in results:    
        output_list.append({
            "id": str(result.id),
            "name":result.name,
            "email":result.email,
            "phone":result.phone,
            "school":{
                "id": str(result.school.id),
                "name":result.school.name,
                "email":result.school.email,
                "phone":result.school.phone,
            }
        })
   
    return output_list


def getTeacherByAdmin(engine: Session, id: str, name:str, email : str, phone:str):
    
   
    
    if len(id.replace("-","")) != 32:
        statement = select(models.Teacher).where(
                # defining filters
                # models.Teacher.school_id == school.id,
                models.Teacher.name.like(f"%{name}%"), 
                models.Teacher.email.like(f"%{email}%"), 
                models.Teacher.phone.like(f"%{phone}%")
            ).options(selectinload(models.Teacher.school))
        
    else:
        statement = select(models.Teacher).where(
                models.Teacher.id == uuid.UUID(id), # id must be fixed
                # models.Teacher.school_id == school.id,
                models.Teacher.name.like(f"%{name}%"), 
                models.Teacher.email.like(f"%{email}%"), 
                models.Teacher.phone.like(f"%{phone}%"),
            ).options(selectinload(models.Teacher.school))
    
    
   
    results = engine.exec(statement)
    
    output_list = list()
    for result in results:    
        output_list.append({
            "id": str(result.id),
            "name":result.name,
            "email":result.email,
            "phone":result.phone,
            "school":{
                "id": str(result.school.id),
                "name":result.school.name,
                "email":result.school.email,
                "phone":result.school.phone,
            }
        })
   
    return output_list

# Update Teacher User
def updateTeacherUser(engine: Session, teacher: models.Teacher):
    statement = select(models.Teacher).where(models.Teacher.id == uuid.UUID(teacher.id))
    results = engine.exec(statement)
    teacher_user = results.one()
    
    if teacher.password != "":
        teacher_user.password = teacher.password
    
    teacher_user.name = teacher.name
    teacher_user.email = teacher.email
    teacher_user.phone = teacher.phone
    
    engine.add(teacher_user)
    engine.commit()
    engine.refresh(teacher_user)
    print("Updated Teacher: ", teacher_user)
    
    
    
    updated_user =  dict(teacher_user)
    updated_user['id'] = str(updated_user['id'])
    updated_user['school_id'] = str(updated_user['school_id'])
    updated_user.pop('password', None)
    # updated_user.pop('created_by', None)
    updated_user['school'] = {
                "id": str(teacher_user.school.id),
                "name":teacher_user.school.name,
                "email":teacher_user.school.email,
                "phone":teacher_user.school.phone,
            }
    return updated_user

# Delete Teacher User
def deleteTeacherUser(engine: Session, teacher: models.Teacher):
    statement = select(models.Teacher).where(
        models.Teacher.id == uuid.UUID(teacher.id),
        models.Teacher.name == teacher.name,
        models.Teacher.email  == teacher.email,
        models.Teacher.phone == teacher.phone
        )
    results = engine.exec(statement)
    teacher_user = results.one()
    
    print("selected teacher_user: ", teacher_user)
    engine.delete(teacher_user)
    engine.commit()
    
    deleted_user =  dict(teacher_user)
    deleted_user['id'] = str(deleted_user['id'])
    deleted_user['school_id'] = str(deleted_user['school_id'])
    deleted_user.pop('password', None)
    
    deleted_user['school'] = {
                "id": str(teacher_user.school.id),
                "name":teacher_user.school.name,
                "email":teacher_user.school.email,
                "phone":teacher_user.school.phone,
            }
    return deleted_user


# Create Student User
def createStudentUser(engine: Session, schooluser: models.School, studentuser: models.Student, password: str, classsection: models.ClassSection):
    print("classsection: ", classsection)
    db_user = models.Student(
        name = studentuser.name,
        password = password,
        email= studentuser.email,
        phone= studentuser.phone,
        school= schooluser,
        school_id = schooluser.id,
        classsection=classsection,
        classsection_id= classsection.id
    )
    
    print("classsection: ", classsection)
    
    engine.add(db_user)
    engine.commit()
    engine.refresh(db_user)
    return db_user

# Get Student User
def getStudentUser(engine: Session, id: str, name:str, email : str, phone:str, school: models.School):
    
    if len(id.replace("-","")) != 32:
        statement = select(models.Student).where(
                # defining filters
                models.Student.school_id == school.id,
                models.Student.name.like(f"%{name}%"), 
                models.Student.email.like(f"%{email}%"), 
                models.Student.phone.like(f"%{phone}%")
            ).options(selectinload(models.Student.school))
        
    else:
        statement = select(models.Student).where(
                models.Student.id == uuid.UUID(id), # id must be fixed
                models.Student.school_id == school.id,
                models.Student.name.like(f"%{name}%"), 
                models.Student.email.like(f"%{email}%"), 
                models.Student.phone.like(f"%{phone}%"),
            ).options(selectinload(models.Student.school))
    
    
   
    results = engine.exec(statement)
    
    output_list = list()
    for result in results:    
        output_list.append({
            "id": str(result.id),
            "name":result.name,
            "email":result.email,
            "phone":result.phone,
            "school":{
                "id": str(result.school.id),
                "name":result.school.name,
                "email":result.school.email,
                "phone":result.school.phone,
            }
        })
   
    return output_list


def getStudentByAdmin(engine: Session, id: str, name:str, email : str, phone:str):
    
    if len(id.replace("-","")) != 32:
        statement = select(models.Student).where(
                # defining filters
                # models.Student.school_id == school.id,
                models.Student.name.like(f"%{name}%"), 
                models.Student.email.like(f"%{email}%"), 
                models.Student.phone.like(f"%{phone}%")
            ).options(selectinload(models.Student.school))
        
    else:
        statement = select(models.Student).where(
                models.Student.id == uuid.UUID(id), # id must be fixed
                # models.Student.school_id == school.id,
                models.Student.name.like(f"%{name}%"), 
                models.Student.email.like(f"%{email}%"), 
                models.Student.phone.like(f"%{phone}%"),
            ).options(selectinload(models.Student.school))
    
    
   
    results = engine.exec(statement)
    
    output_list = list()
    for result in results:    
        output_list.append({
            "id": str(result.id),
            "name":result.name,
            "email":result.email,
            "phone":result.phone,
            "school":{
                "id": str(result.school.id),
                "name":result.school.name,
                "email":result.school.email,
                "phone":result.school.phone,
            }
        })
   
    return output_list

# Update Student User
def updateStudentUser(engine: Session, student: models.Student):
    statement = select(models.Student).where(models.Student.id == uuid.UUID(student.id))
    results = engine.exec(statement)
    student_user = results.one()
    
    if student.password != "":
        student_user.password = student.password
    
    student_user.name = student.name
    student_user.email = student.email
    student_user.phone = student.phone
    
    engine.add(student_user)
    engine.commit()
    engine.refresh(student_user)
    print("Updated Student: ", student_user)
    
    
    
    updated_user =  dict(student_user)
    updated_user['id'] = str(updated_user['id'])
    updated_user['school_id'] = str(updated_user['school_id'])
    updated_user.pop('password', None)
    # updated_user.pop('created_by', None)
    updated_user['school'] = {
                "id": str(student_user.school.id),
                "name":student_user.school.name,
                "email":student_user.school.email,
                "phone":student_user.school.phone,
            }
    return updated_user

# Delete Student User
def deleteStudentUser(engine: Session, student: models.Student):
    statement = select(models.Student).where(
        models.Student.id == uuid.UUID(student.id),
        models.Student.name == student.name,
        models.Student.email  == student.email,
        models.Student.phone == student.phone
        )
    results = engine.exec(statement)
    student_user = results.one()
    
    print("selected teacher_user: ", student_user)
    engine.delete(student_user)
    engine.commit()
    
    deleted_user =  dict(student_user)
    deleted_user['id'] = str(deleted_user['id'])
    deleted_user['school_id'] = str(deleted_user['school_id'])
    deleted_user.pop('password', None)
    
    deleted_user['school'] = {
                "id": str(student_user.school.id),
                "name":student_user.school.name,
                "email":student_user.school.email,
                "phone":student_user.school.phone,
            }
    return deleted_user





# Create ClassSection
def createClassSection(engine: Session, classname: str, schooluser: models.School, teacheruser: models.Teacher):
    db_item = models.ClassSection(
        classname = classname,
        school = schooluser,
        school_id = schooluser.id,
        classteacher = teacheruser,
        classteacher_id = teacheruser.id
    )
    
    engine.add(db_item)
    engine.commit()
    engine.refresh(db_item)
    return db_item

# Get ClassSection
def getClassSection(engine: Session, id: str, classname: str, school: models.School, classteacher: models.Teacher):
    
    
        
    # else:
    #     statement = select(models.ClassSection).where(
    #             models.ClassSection.id == uuid.UUID(id), # id must be fixed
    #             models.ClassSection.school_id == school.id,
    #             models.ClassSection.name.like(f"%{name}%"), 
    #             models.ClassSection.email.like(f"%{email}%"), 
    #             models.ClassSection.phone.like(f"%{phone}%"),
    #         ).options(selectinload(models.ClassSection.school))
    
    statement = select(models.ClassSection)
    
    
    # Filters list
    filters = list()
    
    # if len(id.replace("-","")) == 32: # record id
    print(f"id: {id}, school.id: {school.id}, classteacher.id: {classteacher.id}")
    if id != "*":
        filters.append(models.ClassSection.id == uuid.UUID(id))
        
    if school.id:
        filters.append(models.ClassSection.school_id == school.id)
        
    if classteacher.id:
        filters.append(models.ClassSection.classteacher_id == classteacher.id)
        
    if classname != "*":
        filters.append(models.ClassSection.classname == classname)
    
    # Apply filters only if they exist
    if filters:
        statement = statement.where(*filters)
        
    
    # Optionally preload relationships
    statement = statement.options(
        selectinload(models.ClassSection.school),
        selectinload(models.ClassSection.classteacher),
    )
        
        
    
    
   
    results = engine.exec(statement)
    
    output_list = list()
    for result in results:    
        output_list.append({
            "id": str(result.id),
            "classname":result.classname,
            # "email":result.email,
            # "phone":result.phone,
            "school":{
                "id": str(result.school.id),
                "name":result.school.name,
                "email":result.school.email,
                "phone":result.school.phone,
            },
            "classteacher": {
                "id": str(result.classteacher.id),
                "name": result.classteacher.name,
                "email": result.classteacher.email,
                "phone": result.classteacher.phone,
                "school":{
                    "id": str(result.classteacher.school.id),
                    "name":result.classteacher.school.name,
                    "email":result.classteacher.school.email,
                    "phone":result.classteacher.school.phone,
            },
                
            }
        })
   
    return output_list

#

# Update ClassSection
def updateClassSection(engine: Session, classsection: models.ClassSection):
    statement = select(models.ClassSection).where(models.ClassSection.id == uuid.UUID(classsection.id))
    results = engine.exec(statement)
    classsection_record = results.one()

    
    classsection_record.classname = classsection.classname
    classsection_record.school = classsection.school
    classsection_record.school_id = classsection.school.id
    classsection_record.classteacher = classsection.classteacher
    classsection_record.classteacher_id = classsection.classteacher.id
    
    
    engine.add(classsection_record)
    engine.commit()
    engine.refresh(classsection_record)
    print("Updated classSection: ", classsection_record)
    
    
    
    updated_classsection =  dict(classsection_record)
    updated_classsection['id'] = str(updated_classsection['id'])
    updated_classsection['school_id'] = str(updated_classsection['school_id'])
    updated_classsection['classteacher_id'] = str(updated_classsection['classteacher_id'])
    # updated_user.pop('created_by', None)
    updated_classsection['school'] = {
                "id": str(classsection_record.school.id),
                "name":classsection_record.school.name,
                "email":classsection_record.school.email,
                "phone":classsection_record.school.phone,
            }
    updated_classsection['classteacher'] = {
                "id": str(classsection_record.classteacher.id),
                "name":classsection_record.classteacher.name,
                "email":classsection_record.classteacher.email,
                "phone":classsection_record.classteacher.phone,
            }
    return updated_classsection



# Delete ClassSection
def deleteClassSection(engine: Session, classsection_id: str):
    statement = select(models.ClassSection).where(
        models.ClassSection.id == uuid.UUID(classsection_id),
        # models.ClassSection.classname == classsection.classname,
        # models.ClassSection.school_id  == uuid.UUID(classsection.school_id),
        # models.ClassSection.classteacher_id == uuid.UUID(classsection.classteacher_id)
        )
    results = engine.exec(statement)
    classsection_record = results.one()
    
    print("selected classsection_record: ", classsection_record)
    engine.delete(classsection_record)
    engine.commit()
    
    deleted_record =  dict(classsection_record)
    deleted_record['id'] = str(deleted_record['id'])
    deleted_record['school_id'] = str(deleted_record['school_id'])
    deleted_record['classteacher_id'] = str(deleted_record['classteacher_id'])
    
    
    deleted_record['school'] = {
                "id": str(classsection_record.school.id),
                "name":classsection_record.school.name,
                "email":classsection_record.school.email,
                "phone":classsection_record.school.phone,
            }
    
    deleted_record['classteacher'] = {
                "id": str(classsection_record.classteacher.id),
                "name":classsection_record.classteacher.name,
                "email":classsection_record.classteacher.email,
                "phone":classsection_record.classteacher.phone,
            }
    return deleted_record

# End ClassSection



# Attendance
# Create Attendance
from datetime import datetime as dt, date

def createAttendance(engine: Session, attendance: models.Attendance):
    current_time = dt.now()
    db_item = models.Attendance(
        attendance_date = date(year=current_time.year, month=current_time.month, day = current_time.day),
        attendance_status = attendance.attendance_status,
        
        student_id = uuid.UUID(attendance.student_id),
        classsection_id = uuid.UUID(attendance.classsection_id),
        teacher_id = uuid.UUID(attendance.teacher_id),
        
        student_name = attendance.student_name,
        class_name = attendance.class_name,
        teacher_name = attendance.teacher_name,
        
        school_id = attendance.school_id,
        school = attendance.school
    )
    
    engine.add(db_item)
    engine.commit()
    engine.refresh(db_item)
    return db_item

# Get Attendance
from datetime import date

def getAttendance(engine: Session, id: str, attendance_status: str, attendance_date: date, student_name: str, class_name: str, teacher_name: str, school: models.School):
    
    # Search basis: timestamp, status, student name, class name, teacher name, school id
        
    statement = select(models.Attendance)
    
    
    # Filters list
    filters = list()
    
    
    # Record id
    # print("id is: ",)
    if id != "*":
        filters.append(models.Attendance.id == uuid.UUID(id))
        
    if school.id:
        filters.append(models.Attendance.school_id == school.id)
        
    if teacher_name != "*":
        filters.append(models.Attendance.teacher_name.like(f"%{teacher_name}%"))
        
    if class_name != "*":
        filters.append(models.Attendance.class_name.like(f"%{class_name}%"))
    
    if student_name != "*":
        filters.append(models.Attendance.student_name.like(f"%{student_name}%"))
        
    if attendance_date !="*":
        date_list = attendance_date.split("-")
        filters.append(models.Attendance.attendance_date == date(int(date_list[0]), int(date_list[1]), int(date_list[2])))
    
    if attendance_status != "*":
        filters.append(models.Attendance.attendance_status.like(f"%{attendance_status}%"))
        
        
    
    # Apply filters only if they exist
    if filters:
        statement = statement.where(*filters)
        
    
    # Optionally preload relationships
    statement = statement.options(
        selectinload(models.Attendance.school),
    )
        
    results = engine.exec(statement)
    
    output_list = list()
    for result in results:    
        output_list.append({
            "id": str(result.id),
            "attendance_date":str(result.attendance_date),
            "status":result.attendance_status,
            "student_name":result.student_name,
            "class_name":result.class_name,
            "teacher_name":result.teacher_name,
            "school":{
                "id": str(result.school.id),
                "name":result.school.name,
                "email":result.school.email,
                "phone":result.school.phone,
            },
            
        })
   
    return output_list

# #

# Update Attendance
def updateAttendance(engine: Session, attendance: models.Attendance):
    statement = select(models.Attendance).where(models.Attendance.id == uuid.UUID(attendance.id))
    results = engine.exec(statement)
    attendance_record = results.one()

    
    attendance_record.attendance_status = attendance.attendance_status
    # classsection_record.school = classsection.school
    # classsection_record.school_id = classsection.school.id
    # classsection_record.classteacher = classsection.classteacher
    # classsection_record.classteacher_id = classsection.classteacher.id
    
    
    engine.add(attendance_record)
    engine.commit()
    engine.refresh(attendance_record)
    print("Updated classSection: ", attendance_record)
    
    
    
    updated_attendance =  dict(attendance_record)
    updated_attendance['id'] = str(updated_attendance['id'])
    updated_attendance['school_id'] = str(updated_attendance['school_id'])
    updated_attendance['teacher_id'] = str(updated_attendance['teacher_id'])
    updated_attendance['classsection_id'] = str(updated_attendance['classsection_id'])
    updated_attendance['student_id'] = str(updated_attendance['student_id'])
    updated_attendance['attendance_date'] = str(updated_attendance['attendance_date'])
    
    
    
    # updated_user.pop('created_by', None)
    updated_attendance['school'] = {
                "id": str(attendance_record.school.id),
                "name":attendance_record.school.name,
                "email":attendance_record.school.email,
                "phone":attendance_record.school.phone,
            }
    
    return updated_attendance



# Delete Attendance
def deleteAttendance(engine: Session, id: str):
    statement = select(models.Attendance).where(
        models.Attendance.id == uuid.UUID(id),
        # models.ClassSection.classname == classsection.classname,
        # models.ClassSection.school_id  == uuid.UUID(classsection.school_id),
        # models.ClassSection.classteacher_id == uuid.UUID(classsection.classteacher_id)
        )
    results = engine.exec(statement)
    attendance_record = results.one()
    
    print("selected attendance_record: ", attendance_record)
    engine.delete(attendance_record)
    engine.commit()
    
    deleted_record =  dict(attendance_record)
    deleted_record['id'] = str(deleted_record['id'])
    deleted_record['school_id'] = str(deleted_record['school_id'])
    deleted_record['teacher_id'] = str(deleted_record['teacher_id'])
    deleted_record['student_id'] = str(deleted_record['student_id'])
    deleted_record['classsection_id'] = str(deleted_record['classsection_id'])
    deleted_record['attendance_date'] = str(deleted_record['attendance_date'])
    
    
    deleted_record['school'] = {
                "id": str(attendance_record.school.id),
                "name":attendance_record.school.name,
                "email":attendance_record.school.email,
                "phone":attendance_record.school.phone,
            }
    
    return deleted_record
# End Attendance


# FeePlan
# Create FeePlan
# from datetime import datetime as dt, date

def createFeePlan(engine: Session, feeplan: models.FeePlan):
    
    mydate = feeplan.alert_date.split("-")
    year = int(mydate[0])
    month = int(mydate[1])
    
    
    # month = 
    db_item = models.FeePlan(
        
        school = feeplan.school,
        school_id = feeplan.school_id,
        
        classsection_id = uuid.UUID(feeplan.classsection_id),
        class_name = feeplan.class_name,
        
        fee = feeplan.fee,
        
        alert_date= date(year=year, month = month, day=1)
    )
    
    engine.add(db_item)
    engine.commit()
    engine.refresh(db_item)
    return db_item

# Get FeePlan
# from datetime import date

def getFeePlan(engine: Session, id: str, classsection_id: str, class_name: str, fee: str, alert_date: str, school=models.School):
    
    # Search basis: classsection_id, class_name, fee, school_id, alert_date
        
    statement = select(models.FeePlan)
    
    
    # Filters list
    filters = list()
    
    
    # Record id
    # print("id is: ",)
    if id != "*":
        filters.append(models.FeePlan.id == uuid.UUID(id))
        
    if school.id:
        filters.append(models.FeePlan.school_id == school.id)
        
    if classsection_id != "*":
        filters.append(models.FeePlan.classsection_id == uuid.UUID(classsection_id))
        
        
    if class_name != "*":
        filters.append(models.FeePlan.class_name.like(f"%{class_name}%"))
    
    if fee != "*":
        # need to think for this as > < == range etc.
        # filters.append(models.Attendance.student_name.like(f"%{student_name}%"))
        pass
        
    if alert_date !="*":
        date_list = alert_date.split("-")
        filters.append(models.FeePlan.attendance_date == date(int(date_list[0]), int(date_list[1]), int(date_list[2])))
    
    
        
        
    
    # Apply filters only if they exist
    if filters:
        statement = statement.where(*filters)
        
    
    # Optionally preload relationships
    statement = statement.options(
        selectinload(models.FeePlan.school),
    )
        
    results = engine.exec(statement)
    
    output_list = list()
    for result in results:    
        output_list.append({
            "id": str(result.id),
            "classsection_id":str(result.classsection_id),
            "class_name":result.class_name,
            "fee":float(result.fee),
            "alert_date":str(result.alert_date),
            "school":{
                "id": str(result.school.id),
                "name":result.school.name,
                "email":result.school.email,
                "phone":result.school.phone,
            },
            
        })
   
    return output_list



# Update FeePlan
def updateFeePlan(engine: Session, feeplan: models.FeePlan):
    statement = select(models.FeePlan).where(models.FeePlan.id == uuid.UUID(feeplan.id))
    results = engine.exec(statement)
    feeplan_record = results.one()
    
    feeplan_record.fee = feeplan.fee

    
    
    
    
    engine.add(feeplan_record)
    engine.commit()
    engine.refresh(feeplan_record)
    print("Updated Fee Plan: ", feeplan_record)
    
    
    
    updated_feeplan =  dict(feeplan_record)
    updated_feeplan['id'] = str(updated_feeplan['id'])
    updated_feeplan['school_id'] = str(updated_feeplan['school_id'])
    updated_feeplan['classsection_id'] = str(updated_feeplan['classsection_id'])
    updated_feeplan['class_name'] = str(updated_feeplan['class_name'])
    updated_feeplan['fee'] = str(updated_feeplan['fee'])
    updated_feeplan['alert_date'] = str(updated_feeplan['alert_date'])
    
    
    
    # updated_user.pop('created_by', None)
    updated_feeplan['school'] = {
                "id": str(feeplan_record.school.id),
                "name":feeplan_record.school.name,
                "email":feeplan_record.school.email,
                "phone":feeplan_record.school.phone,
            }
    
    return updated_feeplan



# Delete FeePlan
def deleteFeePlan(engine: Session, id: str):
    statement = select(models.FeePlan).where(
        models.FeePlan.id == uuid.UUID(id),
    )
    
    results = engine.exec(statement)
    feeplan_record = results.one()
    
    print("selected feeplan_record: ", feeplan_record)
    engine.delete(feeplan_record)
    engine.commit()
    
    deleted_record =  dict(feeplan_record)
    deleted_record['id'] = str(deleted_record['id'])
    deleted_record['school_id'] = str(deleted_record['school_id'])
    deleted_record['classsection_id'] = str(deleted_record['classsection_id'])
    deleted_record['alert_date'] = str(deleted_record['alert_date'])
    
    
    deleted_record['school'] = {
                "id": str(feeplan_record.school.id),
                "name":feeplan_record.school.name,
                "email":feeplan_record.school.email,
                "phone":feeplan_record.school.phone,
            }
    
    return deleted_record
# End FeePlan



# Fee
# Create Fee
# from datetime import datetime as dt, date

def createFeeRecord(engine: Session, feerecord: models.FeeRecord):
    
    db_item = models.FeeRecord(
        
        school = feerecord.school,
        school_id = feerecord.school_id,
        
        student_id = uuid.UUID(feerecord.student_id),
        student_name = feerecord.student_name,
        
        feeplain_id = feerecord.feeplan_id,
        
        paid = feerecord.paid,
        
        payment_timestamp = dt.now()
    )
    
    engine.add(db_item)
    engine.commit()
    engine.refresh(db_item)
    return db_item

# Get FeeRecord
# from datetime import date

def getFeeRecord(engine: Session, id: str, student_id: str, student_name: str, feeplan_id: str, paid: bool, payment_timestamp: str, school=models.School):
    
    # Search basis: classsection_id, class_name, fee, school_id, alert_date
        
    statement = select(models.FeeRecord)
    
    
    # Filters list
    filters = list()
    
    
    # Record id
    # print("id is: ",)
    if id != "*":
        filters.append(models.FeeRecord.id == uuid.UUID(id))
        
    if school.id:
        filters.append(models.FeeRecord.school_id == school.id)
        
    if student_id != "*":
        filters.append(models.FeeRecord.student_id == uuid.UUID(student_id))
        
        
    if student_name != "*":
        filters.append(models.FeeRecord.student_name.like(f"%{student_name}%"))
    
    if feeplan_id != "*":
        filters.append(models.FeeRecord.feeplan_id == uuid.UUID(feeplan_id))
        
    
    
    # Apply filters only if they exist
    if filters:
        statement = statement.where(*filters)
        
    
    # Optionally preload relationships
    statement = statement.options(
        selectinload(models.FeeRecord.school),
    )
        
    results = engine.exec(statement)
    
    output_list = list()
    for result in results:    
        output_list.append({
            "id": str(result.id),
            "student_id":str(result.student_id),
            "student_name":result.class_name,
            "feeplan_id":str(result.feeplan_id),
            "paid":result.paid, 
            "payment_timestamp":str(result.payment_timestamp),
            "school":{
                "id": str(result.school.id),
                "name":result.school.name,
                "email":result.school.email,
                "phone":result.school.phone,
            },
            
        })
   
    return output_list



# Update FeeRecord
def updateFeeRecord(engine: Session, feerecord: models.FeeRecord):
    statement = select(models.FeeRecord).where(models.FeeRecord.id == uuid.UUID(feerecord.id))
    results = engine.exec(statement)
    fee_record = results.one()
    
    fee_record.paid = feerecord.paid

    
    
    
    
    engine.add(fee_record)
    engine.commit()
    engine.refresh(fee_record)
    print("Updated Fee Plan: ", fee_record)
    
    
    
    updated_feerecord =  dict(fee_record)
    updated_feerecord['id'] = str(updated_feerecord['id'])
    updated_feerecord['school_id'] = str(updated_feerecord['school_id'])
    updated_feerecord['student_id'] = str(updated_feerecord['student_id'])
    updated_feerecord['feeplan_id'] = str(updated_feerecord['feeplan_id'])
    updated_feerecord['payment_timestamp'] = str(updated_feerecord['payment_timestamp'])
    
    
    
    # updated_user.pop('created_by', None)
    updated_feerecord['school'] = {
                "id": str(fee_record.school.id),
                "name":fee_record.school.name,
                "email":fee_record.school.email,
                "phone":fee_record.school.phone,
            }
    
    return updated_feerecord



# Delete FeePlan
def deleteFeeRecord(engine: Session, id: str):
    statement = select(models.FeeRecord).where(
        models.FeeRecord.id == uuid.UUID(id),
    )
    
    results = engine.exec(statement)
    fee_record = results.one()
    
    print("selected fee_record: ", fee_record)
    engine.delete(fee_record)
    engine.commit()
    
    deleted_record =  dict(fee_record)
    deleted_record['id'] = str(deleted_record['id'])
    deleted_record['school_id'] = str(deleted_record['school_id'])
    deleted_record['student_id'] = str(deleted_record['student_id'])
    deleted_record['feeplan_id'] = str(deleted_record['feeplan_id'])
    deleted_record['payment_timestamp'] = str(deleted_record['payment_timestamp'])

    
    
    deleted_record['school'] = {
                "id": str(fee_record.school.id),
                "name":fee_record.school.name,
                "email":fee_record.school.email,
                "phone":fee_record.school.phone,
            }
    
    return deleted_record
# End FeePlan
