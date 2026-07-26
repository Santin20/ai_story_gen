from flask import Blueprint, render_template, request, redirect, url_for,session,flash
import smtplib
import ssl
from email.message import EmailMessage
from dotenv import load_dotenv
import random
from otp import Otp,Otp1
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
                session["uid"]=data[2]
                return redirect(url_for("dash.dash_board"))
            else:
                return render_template("sign_in.html",i="true")
        else:

            if(email!=None):
                return render_template("sign_in.html",i="true")
            else:
                return render_template("sign_in.html")
    except Exception as e:
        print(email)
        if(email!=None):
            return render_template("sign_in.html",i="true")
        else:
            return render_template("sign_in.html")
    
    return render_template("sign_in.html")


@sign.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":

        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        otp1 = random.randint(100000, 999999)
        
        session["user"]=[otp1,name,email,password]
        Otp(name,otp1,email)
        return redirect(url_for('sign.otp'))

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
                return redirect(url_for("sign.signin_page"))
            except Exception as e:
                print(e)
                if e.errno == 1062:

                    flash("Email already exists.", "error")
                    return redirect(url_for("sign.signin_page"))
                    print("EMAIL ALREADY EXISTS")
                
    return render_template("otp_verification.html")

@sign.route("/forgot_password",methods=["POST","GET"])
def forget():
    if(request.method=="POST"):
        email=request.form.get("email")
        session["mail_id"]=email
        print("email")
        session["fotp"]=random.randint(100000,999999)
        Otp1(session.get("fotp"),email)
        return redirect(url_for("sign.fotp_v"))
    return render_template("forget_pass.html")
@sign.route("/verify_otp1",methods=["POST","GET"])
def fotp_v():
    if(request.method=='POST'):
        inotp=request.form.get("otp")
        print(inotp)
        if(int(inotp)==int(session.get("fotp"))):
            return redirect(url_for("sign.reset"))
        else:
            return render_template("otp_verification1.html",i="w")
    return render_template("otp_verification1.html")
@sign.route("/reset_pass",methods=["POST","GET"])
def reset():
    if(request.method=="POST"):
        mydb=connection()
        cur=mydb.cursor()
        mail_id=session.get("mail_id")
        password=request.form.get("password")
        cur.execute("update clients set password=%s where mail=%s",(password,mail_id))
        mydb.commit()
        return redirect(url_for("dash.dash_board"))
    return render_template("reset_pass.html")