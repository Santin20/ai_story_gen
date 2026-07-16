from flask import Blueprint, render_template, request, redirect, url_for,session
from google import genai
from dotenv import load_dotenv
import os
from sql import connection
load_dotenv()
ai=genai.Client(api_key=os.getenv("key"))
dash=Blueprint("dash",__name__)
@dash.route("/dash",methods=["GET","POST"])
def dash_board():
    user=session.get("profile")
    fun=request.args.get("fun")
    if(request.method=="POST"):
        val=request.form.get("gen")
        if(val=='hint'):
            data=request.form.getlist("hints")
            lang=request.form.get("lang")
            limit=request.form.get("limit")
            story_type=request.form.get("story_type")
            response = ai.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=f'''{data} I HAVE GIVEN YOU LIST OF hint FROM user PLEASE GIVE user
            A {story_type} story less than {limit} words in {lang} language note that the story generated want to have a clear starting and ending
            jumps should be connected ,add orginality
            IF LIST IS EMPTY OR NO DATA GIVEN PLEASE PRINT NO DATA GIVEN (NOTE:IT SHOULD NOT BE KNOWN AI GENERATED) PLEASE REMOVE INTRO OF QUERY")''')
            session["story"]=response.text
            return render_template("dashbord.html",i=user,fun='hint',story=session.get("story"))
        elif(val=='draft'):
            data=request.form.get("draft_story")
            lang=request.form.get("lang")
            limit=request.form.get("limit")
            story_type=request.form.get("story_type")
            response = ai.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=f'''{data} I HAVE GIVEN YOU DRAFT OF A STORY FROM user PLEASE GIVE user
            A {story_type} story less than {limit} words in {lang} language note that the story generated want to have a clear starting and ending
            jumps should be connected AND IN MORE ATTRACTIVE WAY,add orginality
            IF LIST IS EMPTY OR NO DATA GIVEN PLEASE PRINT NO DATA GIVEN (NOTE:IT SHOULD NOT BE KNOWN AI GENERATED) PLEASE REMOVE INTRO OF QUERY")''')
            session["story"]=response.text
            return render_template("dashbord.html",i=user,fun='draft',story=session.get("story"))
        elif(val=='title'):
            data=request.form.getlist("title")
            lang=request.form.get("lang")
            limit=request.form.get("limit")
            story_type=request.form.get("story_type")
            response = ai.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=f'''{data} I HAVE GIVEN YOU title  FROM user PLEASE GIVE user
            A {story_type} story less than {limit} words in {lang} language note that the story generated want to have a clear starting and ending
            jumps should be connected AND IN MORE ATTRACTIVE WAY,add orginality
            IF LIST IS EMPTY OR NO DATA GIVEN PLEASE PRINT NO DATA GIVEN (NOTE:IT SHOULD NOT BE KNOWN AI GENERATED) PLEASE REMOVE INTRO OF QUERY")''')
            session["story"]=response.text
            return render_template("dashbord.html",i=user,fun='title',story=session.get("story"))
        if(val=='save'):
            print(session.get("profile")[1])
            mydb=connection()
            cur=mydb.cursor()
            cur.execute("insert into save_stories values (%s,%s)",(session.get("profile")[1],session.get("story"),))
            mydb.commit()
            return render_template("dashbord.html",i=user,fun='hint',story=session.get("story"))
    return render_template("dashbord.html",i=user,fun=fun)
