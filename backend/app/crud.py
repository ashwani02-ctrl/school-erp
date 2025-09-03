from sqlmodel import select, Session
from .models import Admin


def getUserByEmail(engine, email: str):
    statement = select(Admin).where(Admin.email==email)
    
    user = engine.exec(statement = statement).first() # engine is already a session, so we don't need to do Session(engine)
       
    return user
    


    