import smtplib
import ssl
from email.message import EmailMessage
from dotenv import load_dotenv
import os


def Mail(reciver,subject,message):
    load_dotenv()

    try:
        email_sender= os.getenv("EMAIL")
        email_password= os.getenv("PASSWORD")
        email_reciver=reciver
        subject=subject
        body=message
        em=EmailMessage()
        em['From']= email_sender
        em['To']=email_reciver
        em['Subject']=subject
        em.set_content(body)
        context=ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com',465,context=context)as smtp:
            smtp.login(email_sender,email_password)
            smtp.sendmail(email_sender,email_reciver,em.as_string())
    except smtplib.SMTPException as e:
        return False, f"SMTP Error: {e}"
    except Exception as error:
        return error
      
