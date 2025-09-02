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

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="Authorization")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_session)):
    decoded_token = decoding(token)
    # print(type(decoded_token["data"]))
    print(db)
    # user = crud.get_user_by_id(db=db, user_id=decoded_token["data"])
    # if not user:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Invalid authentication credentials",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )
    # return user
    # return user
    return {"message":"Hello, World!"}


@app.get("/")
async def root():
	return {"message":"Hello, World!"}


from .security.passwordhashing import random_password_generator

# Creating Admin (SuperUser) user API
# @app.post("/api/admin", response_model = models.Admin)
# async def createAdminUser(admin: models.Admin):
#     print("admin: ", admin)
#     return JSONResponse(content={"message":"API Working!"}, status_code=status.HTTP_200_OK)



# Admin user Login
# from crud import getUserByEmail

@app.post("/api/admin/login", response_model = models.Admin)
async def loginAdminUser(admin: models.Admin, db: Session = Depends(get_session)):
    
    get_user = crud.getUserByEmail(db, admin.email, admin.password)
    print(get_user)
    return JSONResponse(content={"message":"API Working!"}, status_code=status.HTTP_200_OK)



if __name__ == "__main__":
    print(get_session())
