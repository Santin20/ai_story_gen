from mail import Mail
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

def Otp1(otp,mail):
    sub = "APS AI STORY GEN - Password Reset OTP"
    content = f"""
    Hello,

    We received a request to reset the password for your APS AI STORY GEN account.

    Your One-Time Password (OTP) for password reset is:

    {otp}

    This OTP is valid for 10 minutes.

    Please do not share this OTP with anyone.

    If you did not request a password reset, you can safely ignore this email. Your account will remain secure.

    Regards,
    APS AI STORY GEN Team
    """
    Mail(mail,sub,content)
    