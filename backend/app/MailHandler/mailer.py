# from json import load
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
import enum
load_dotenv()

# Defining the types of Emails to be sent
class EmailType(enum.Enum):
    NEW_USER_REGISTRATION = "new_user_registration"
    # UNIVERSITY = "University"
    # STUDENT = "Student"
    # PLACEMENT = "Placement"
    
EmailSubject={
    'NEW_USER_REGISTRATION' : "Welcome to Abhishek Roka's School ERP System"
    
}
    # UNIVERSITY = "University"
    # STUDENT = "Student"
    # PLACEMENT = "Placement"
    
def send_email(email_type, recipient_email,  subject, message_variables, username=None):
    # Your Gmail credentials
    sender_email = os.environ['EMAIL_ID']
    sender_password = os.environ['EMAIL_PASSWORD']
    # print(sender_password)

    # Create the email message
    subject = str(subject)
    
    if email_type == EmailType.NEW_USER_REGISTRATION:
        with open("./MailHandler/Templates/PasswordGenerated.txt", "r", encoding="utf-8") as file:
            message = file.read()
            message = message.replace("{Your Portal Name}", os.environ['PORTAL_NAME'])
            message = message.replace("{username}", message_variables['username'])
            message = message.replace("{password}", message_variables['password'])
    message = message.replace("{email}", recipient_email)
    message = message.replace("{login_url}", os.environ['PORTAL_URL'])
            
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = recipient_email
    msg["Subject"] = subject
    msg.attach(MIMEText(message, "html"))

    # Connect to Gmail's SMTP server
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())

if __name__=="__main__":
    # Example usage
    message_variables = {
        "username": "JohnDoe",
        "password": "random_password",
    }
    
    # username = "JohnDoe"
    user_id = "12345"
    recipient_email = "rockst463@gmail.com"
    send_email(email_type="new_user_registration", recipient_email=recipient_email, subject="New Joinee", message_variables=message_variables)