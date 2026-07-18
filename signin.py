from flask import Blueprint, render_template, request, redirect, url_for,session,flash
import smtplib
import ssl
from email.message import EmailMessage
from dotenv import load_dotenv
import random
from otp import Otp,test
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
