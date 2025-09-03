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
    # print(decoded_token)
    
    user = crud.get_user_by_id(engine = db, user_id=decoded_token["data"])
    if not user:
        raise Exception(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
    )
    return user
    # return user
    # return {"message":"Hello, World!"}


@app.get("/")
async def root():
	return {"message":"Hello, World!"}

@app.get("/test")
async def test(current_user: Annotated[models.Admin, Depends(get_current_user)], db: Session = Depends(get_session)):
    print("current user is: ",current_user)
    return {"message":"Hello, World!"}


from .security.passwordhashing import hash_password

# Creating Admin (SuperUser) user API
# @app.post("/api/admin", response_model = models.Admin)
# async def createAdminUser(admin: models.Admin):
#     print("admin: ", admin)
#     return JSONResponse(content={"message":"API Working!"}, status_code=status.HTTP_200_OK)



# Admin user Login
# from crud import getUserByEmail

@app.post("/api/admin/login", response_model = models.Admin)
async def loginAdminUser(admin: models.Admin, db: Session = Depends(get_session)):
    
    user = crud.getUserByEmail(db, admin.email)
    if user:
        # Now check the passwords!
        if hash_password(admin.password) == user.password:
            jwt_token = encoding(user.id, "admin")
            return JSONResponse(content={"message": "Login successful!", "token": jwt_token }, status_code=status.HTTP_200_OK)
        else:
            return JSONResponse(content={"message":"Incorrect Password!"}, status_code=status.HTTP_401_UNAUTHORIZED)
    
    return JSONResponse(content={"message":"User not found!"}, status_code=status.HTTP_404_NOT_FOUND)


    



if __name__ == "__main__":
    print(get_session())
