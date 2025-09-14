from fastapi import FastAPI, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from sqlmodel import SQLModel, Session
from . import models, crud

from .database import engine
SQLModel.metadata.create_all(engine)

from typing import Annotated

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
    if not user["user"]:
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
            jwt_token = encoding(db_user.id, "admin")
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
@app.get("/api/admin", response_model=models.Admin)
async def getAdminUser(current_user: Annotated[models.Admin, Depends(get_current_user)], id: str = "*", name: str = "*", email: EmailStr = "*", phone : str="*",  db: Session = Depends(get_session)):
    
    if current_user["role"] == "admin":
        if id=="*":
            id=""
        if name=="*":
            name=""
        if "*" in email:
            email=""
        if phone=="*":
            phone=""
        
        try:
            admin_users = crud.getAdminUser(engine=db, id=id, name=name, email=email, phone=phone)
            return JSONResponse(content={"message":"Operation Successful", "data": admin_users}, status_code=status.HTTP_200_OK)
        
        except Exception as e:
             return JSONResponse(content={"message":f"Error: {e}"}, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    return JSONResponse(content={"message":"You are not authorized for this action."}, status_code=status.HTTP_401_UNAUTHORIZED)


if __name__ == "__main__":
    print(get_session())
