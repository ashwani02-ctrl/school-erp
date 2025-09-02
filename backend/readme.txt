Build sequence

1. Super user creation flow
Needs AdminUSer Table to create user.
requirements:
name: str
email: EmailStr
phone: str = Field(max_length=15)
password: str


2. Superuser auth flow
Need email and password -> then we have the thing
3. Current User flow
4. CRUD user flow
5. CRUD Fee flow
6. CRUD Attendance flow


Flow:-
1. Super user creation
2. Authenticatin of Superuser
3. CRUD Users flow


Superuser
name: admin
password: simple
email: abhishekroka2003@gmail.com
phone: 8907654321