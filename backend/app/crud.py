from sqlmodel import select, Session
from .models import Admin
import uuid

def getUserByEmail(engine, email: str):
    statement = select(Admin).where(Admin.email==email)
    
    user = engine.exec(statement = statement).first() # engine is already a session, so we don't need to do Session(engine)
       
    return user

from uuid import UUID
def get_user_by_id(engine: Session, user_id):
    print("Inside get user by id")
    print("id: ",user_id)
    statement = select(Admin).where(Admin.id==UUID(user_id))
    return engine.exec(statement = statement).first() 
    

    


    