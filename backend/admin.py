import hashlib

from app.models import Admin
from app.database import engine
from sqlmodel import Session
import argparse
from getpass import getpass




if __name__ == "__main__":
    print("I'm admin.py running.")
    
    parser = argparse.ArgumentParser(description="CLI for Admin related settings.")
    parser.add_argument("--createsuperuser", action='store_true', help="Create a superuser")
    
    args = parser.parse_args()
    
    if (args.createsuperuser):
        name = input("Enter super user name: ")
        password = getpass("Enter password: ")
        email = input("Enter email: ")
        phone = input("Enter phone number: ")
        
        # Hash the password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        # Create a new user instance
        new_user = Admin(
            name=name,
            password=hashed_password,
            email=email,
            phone=phone
        )
        
        # Create a session and add the new user to the database
        # db: Session = SessionLocal()
        # db.add(new_user)
        # db.commit()
        # db.refresh(new_user)
        with Session(engine) as session:
            db_admin = Admin.model_validate(new_user)
            session.add(db_admin)
            session.commit()
            session.refresh(db_admin)
        
        
        print(f"Superuser {name} created successfully.")
    