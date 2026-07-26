from flask import Blueprint, render_template, request, redirect, url_for,session
from google import genai
from functools import wraps
from dotenv import load_dotenv
import os
from sql import connection
import asyncio
import os
import edge_tts 
async def generate_audio(text, filename,lang):
    communicate = edge_tts.Communicate(text,lang)
    await communicate.save(filename)
load_dotenv()
lis=[]
ai=genai.Client(api_key=os.getenv("api_key"))
dash=Blueprint("dash",__name__)
@dash.route("/dash",methods=["GET","POST"])
def dash_board():
    
    @wraps(f)
    def wrapper(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("sign.signin"))
        return f(*args, **kwargs)
    return wrapper
    langs= {
    "english": "en-US-GuyNeural",
    "tamil": "ta-IN-ValluvarNeural",
    "malayalam": "ml-IN-MidhunNeural",
    "hindi": "hi-IN-MadhurNeural"
    }
    user=session.get("profile")
    fun=request.args.get("fun")
    if(request.method=="POST"):
        val=request.form.get("gen")
        status=val
        if(val!=None):
            session["val"]=val
        speak=request.form.get("speak")
        lis=[session.get("val"),speak]
        if(lis[0]=='hint'):
            if(status!=None):
                data=request.form.getlist("hints")
                lang=request.form.get("lang")
                limit=request.form.get("limit")
                session["lang"]=lang
                story_type=request.form.get("story_type")
                response = ai.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=f'''{data} I HAVE GIVEN YOU LIST OF hint FROM user PLEASE GIVE user
                A {story_type} story less than {limit} words in {lang} language note that the story generated want to have a clear starting and ending
                jumps should be connected ,add orginality
                IF LIST IS EMPTY OR NO DATA GIVEN PLEASE PRINT NO DATA GIVEN (NOTE:IT SHOULD NOT BE KNOWN AI GENERATED) PLEASE REMOVE INTRO OF QUERY")''')
                session["story"]=response.text
            if(lis[1]=='speak'):
                text =session.get("story")
                lang=langs.get(session.get("lang"))
                asyncio.run(generate_audio(text, "static/audio/output.mp3",lang))
                return render_template("dashbord.html",i=user,fun='hint',story=session.get("story"),aud="ya")                
            return render_template("dashbord.html",i=user,fun='hint',story=session.get("story"))
        elif(lis[0]=='draft'):
            if(status!=None):
                data=request.form.get("draft_story")
                lang=request.form.get("lang")
                limit=request.form.get("limit")
                session["lang"]=lang
                story_type=request.form.get("story_type")
                response = ai.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=f'''{data} I HAVE GIVEN YOU DRAFT OF A STORY FROM user PLEASE GIVE user
                A {story_type} story less than {limit} words in {lang} language note that the story generated want to have a clear starting and ending
                jumps should be connected AND IN MORE ATTRACTIVE WAY,add orginality
                IF LIST IS EMPTY OR NO DATA GIVEN PLEASE PRINT NO DATA GIVEN (NOTE:IT SHOULD NOT BE KNOWN AI GENERATED) PLEASE REMOVE INTRO OF QUERY")''')
                session["story"]=response.text
            if(lis[1]=='speak'):
                text =session.get("story")
                lang=langs.get(session.get("lang"))
                asyncio.run(generate_audio(text, "static/audio/output.mp3",lang))
                return render_template("dashbord.html",i=user,fun='draft',story=session.get("story"),aud="ya")
            return render_template("dashbord.html",i=user,fun='draft',story=session.get("story"))
        elif(lis[0]=='title'):
            if(status!=None):
                data=request.form.getlist("title")
                lang=request.form.get("lang")
                limit=request.form.get("limit")
                session["lang"]=lang
                story_type=request.form.get("story_type")
                response = ai.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=f'''{data} I HAVE GIVEN YOU title  FROM user PLEASE GIVE user
                A {story_type} story less than {limit} words in {lang} language note that the story generated want to have a clear starting and ending
                jumps should be connected AND IN MORE ATTRACTIVE WAY,add orginality
                IF LIST IS EMPTY OR NO DATA GIVEN PLEASE PRINT NO DATA GIVEN (NOTE:IT SHOULD NOT BE KNOWN AI GENERATED) PLEASE REMOVE INTRO OF QUERY")''')
                session["story"]=response.text
            if(lis[1]=='speak'):
                text =session.get("story")
                lang=langs.get(session.get("lang"))
                asyncio.run(generate_audio(text, "static/audio/output.mp3",lang))
                return render_template("dashbord.html",i=user,fun='title',story=session.get("story"),aud="ya")
            return render_template("dashbord.html",i=user,fun='title',story=session.get("story"))
    return render_template("dashbord.html",i=user,fun=fun)
