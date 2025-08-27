from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from sqlmodel import SQLModel, Session
from . import models

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

if __name__ == "__main__":
    print(get_session())
