
import sys
import mysql.connector
from loginmiddleware import loginmid
from tkinter import messagebox
def connect():
    conn = None
    try:
        conn = mysql.connector.connect(host='localhost', port=3306, user='root', password='', database='taxisystem')
        print("Connected!")
    except:
        print("Error: ", sys.exc_info())
    finally:
        return conn

def registerinfo(copy):
    conn = connect()
    mycursor = conn.cursor()
    try:
        insertquery = "INSERT INTO userinfo (name, email,phone_num,password, address) VALUES (%s, %s, %s, %s, %s)"
        values = (copy.getnameid(), copy.getemailmid(), copy.getphonemid(),copy.getpassmid(), copy.getaddressmid())
    
        mycursor.execute(insertquery,values)
        conn.commit()
    except:
        messagebox.showerror(title="error", message="Email already used")
    conn.close()
    mycursor.close()

def logininfo(id,email, password):
    userinput = (email, password)
    conn = connect()
    mycursor = conn.cursor()
    try:
        insertquery = "select Id, email, password from userinfo where email = %s and password = %s" 
    
        mycursor.execute(insertquery,userinput)
    #getting data from sql
        for info in mycursor:
            userid = info[0]
            useremail = info[1]
            userpass = info[2]
  
        return userid
    except:
        messagebox.showerror(title="error", message="wrong password or email")

    conn.close()
    mycursor.close()

  
    




