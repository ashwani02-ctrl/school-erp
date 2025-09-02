from .models import Admin
from pydantic import EmailStr

class AdminLogin(Admin):
    email: EmailStr
    password: str