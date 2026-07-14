import mysql.connector as con
from dotenv import load_dotenv
import os
def connection():
    load_dotenv()
    connect=con.connect(
    host="localhost",
    user=os.getenv("user"),
    port=4000,
    password=os.getenv("sql"),
    database="story",
    charset="utf8mb4")
    return connect
