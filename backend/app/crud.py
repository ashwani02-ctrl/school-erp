from sqlmodel import select, Session
from .models import Admin


def getUserByEmail(engine, email: str, password: str):
    statement = select(Admin).where(Admin.email==email)
    
    results = engine.exec(statement = statement) # engine is already a session, so we don't need to do Session(engine)
    for result in results:
        print(result)
    


    pass