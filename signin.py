from flask import Blueprint, render_template, request, redirect, url_for,session
import smtplib
import ssl
from email.message import EmailMessage
from dotenv import load_dotenv
import random
import os
from sql import connection
sign = Blueprint("sign", __name__)

load_dotenv()


@sign.route("/", methods=["GET", "POST"])
def signin_page():
    email=request.form.get("email")
    password=request.form.get("password")
    try:
        mydb=connection()
        cur=mydb.cursor()
        cur.execute("select * from clients where mail=%s",(email,))
        data=cur.fetchone()
        session["profile"]=data
        if(data!=None):
            if(data[2]==password):
                return redirect(url_for("dash.dash_board"))
    except Exception as e:
        print(e)
    
    return render_template("sign_in.html")


@sign.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        otp = random.randint(100000, 999999)

        try:

            email_sender = os.getenv("EMAIL")
            email_password = os.getenv("PASSWORD")

            em = EmailMessage()

            em["From"] = email_sender
            em["To"] = email
            em["Subject"] = "APS AI STORY GEN - Email Verification OTP"
            print("hi mail")
            em.set_content(f"""
Hello {name},

Thank you for registering with APS AI STORY GEN.

Your One-Time Password (OTP) is:

{otp}

This OTP is valid for 10 minutes.

Please do not share this OTP with anyone.

If you did not create this account, please ignore this email.

Regards,
APS AI STORY GEN Team
""")
             
            context = ssl.create_default_context()

            with smtplib.SMTP_SSL("smtp.gmail.com", 4000, context=context,timeout=20) as smtp:

                smtp.login(email_sender, email_password)

                smtp.send_message(em)
            session["user"]=[otp,name,email,password]
            return redirect(url_for('sign.otp'))
        except smtplib.SMTPRecipientsRefused:
            return "Recipient email address was rejected."
        
        except smtplib.SMTPAuthenticationError:
            return "Invalid sender email or app password."
        except smtplib.SMTPException as e:
            print(e)
            return f"SMTP Error : {e}"

        except Exception as e:
            return f"Error : {e}"

    return render_template("sign_up.html")
@sign.route("/verify_otp",methods=["POST","GET"])
def otp():
    mydb=connection()
    cur=mydb.cursor()
    
    ud=session.get("user")
    print(ud)
    
    if(request.method=="POST"):
        otp_ver=request.form.get('otp')
        print(ud,otp_ver)
        if(int(ud[0])==int(otp_ver)):
            try:
                cur.execute("insert into clients values(%s,%s,%s,%s)",(ud[1],ud[2],ud[3],"100"))
                mydb.commit()
            except Exception as e:
                print(e)
                if e.errno == 1062:
                    print("EMAIL ALREADY EXISTS")
    return render_template("otp_verification.html")
