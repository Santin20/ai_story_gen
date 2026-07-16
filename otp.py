from mail import Mail
import socket
def test():
  import smtplib
  
  print("Connecting...")
  
  smtp = smtplib.SMTP("smtp.gmail.com", 587, timeout=10)
  
  print("Connected")

  smtp.quit()
def Otp(name,otp,mail):
  
    content=f"""
        Hello {name},

        Thank you for registering with APS AI STORY GEN.

        Your One-Time Password (OTP) is:

        {otp}

        This OTP is valid for 10 minutes.

        Please do not share this OTP with anyone.

        If you did not create this account, please ignore this email.

        Regards,
        APS AI STORY GEN Team
        """
    sub="APS AI STORY GEN - Email Verification OTP"
    Mail(mail,sub,content)
