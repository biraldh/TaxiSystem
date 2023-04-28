from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
import sys
import mysql.connector
from tkinter import messagebox
import re

class Driverregistration():
    #initialize
    def __init__(self, regframe):
        self.regframe = regframe
        self.regframe.geometry("800x500")
        self.regframe.configure(bg='#A6F47F')  
        self.regframe.resizable(False,False)
        #frame
        rightframe = Frame(self.regframe,bg='#dfeff0',  width = 450 , height=500).pack(side=RIGHT)
         
        #label/entry
        titlelbl = Label(rightframe, bg='#dfeff0', font= 30 , text="Register").place(x= 550, y= 40)
        
        usernamelbl = Label(rightframe, bg='#dfeff0', text="Fullname")
        usernamelbl.place(x= 477, y= 100)

        self.usernametxt = Entry(rightframe,width= 30)
        self.usernametxt.place(x= 480, y= 120)

        Emaillbl = Label(rightframe,bg='#dfeff0', text="Email")
        Emaillbl.place(x= 477, y= 150)

        self.Emailtxt = Entry(rightframe,width= 30)
        self.Emailtxt.place(x= 480, y= 170)

        passwordlbl = Label(rightframe, bg='#dfeff0', text="Password")
        passwordlbl.place(x= 477, y= 200)

        self.passwordtxt = Entry(rightframe,width= 30, show="*")
        self.passwordtxt.place(x= 480, y= 220)

        Phonenumlbl = Label(rightframe, bg='#dfeff0', text="Phone No")
        Phonenumlbl.place(x= 477, y= 250)

        self.Phonenumtxt = Entry(rightframe,width= 30,)
        self.Phonenumtxt.place(x= 480, y= 270)

        addresslbl = Label(rightframe, bg='#dfeff0', text="Address")
        addresslbl.place(x= 477, y= 300)

        self.addresstxt = Entry(rightframe,width= 30,)
        self.addresstxt.place(x= 480, y= 320)

        Licenselbl = Label(rightframe, bg='#dfeff0', text="Driver License")
        Licenselbl.place(x= 477, y= 350)

        self.Licensetxt = Entry(rightframe,width= 30,)
        self.Licensetxt.place(x= 480, y= 370)

        #buttons
        Register_btn = Button(rightframe,text="Register", width=10, command = self.validation)
        Register_btn.place(x = 540, y = 400)
        
        #image
        img1 = Image.open("taxiwallpage.jpg").resize((400,500))
        self.img = ImageTk.PhotoImage(img1)
        imglabel = Label(regframe, image =self.img)
        imglabel.place(x=0, y =0)
    
    def connect(self):
        conn = None
        try:
            conn = mysql.connector.connect(host='localhost', port=3306, user='root', password='', database='taxisystem')
            print("Connected!")
        except:
            print("Error: ", sys.exc_info())
        finally:
            return conn
   
    def validation(self):
   
        pat = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        self.nameval = self.usernametxt.get()
        self.emailval = self.Emailtxt.get()
        self.passval = self.passwordtxt.get()
        self.phoneval = self.Phonenumtxt.get()
        self.addressval = self.addresstxt.get() 
        self.licenseval = self.Licensetxt.get()            
        if self.nameval =="" or self.emailval == "" or self.passval == "" or self.phoneval == "" or self.addressval == "" or self.licenseval =="":
            messagebox.showerror(title="error", message="fill all the fields")
            
        else:
            if re.match(pat, self.emailval):
                self.sendtodatabase()
            else : 
                messagebox.showerror(title="error", message="Invalid email") 
                
    def sendtodatabase(self):
        conn = self.connect()
        mycursor = conn.cursor()
        try:
            insertquery = "INSERT INTO Driverinfo (name, email,phone_num,password, address,License_plate,Driver_status) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            values = (self.nameval,self.emailval, self.phoneval, self.passval, self.addressval, self.licenseval, "Available")
            mycursor.execute(insertquery,values)
            messagebox.showinfo(title="Success", message="You have been successfully registered")
            conn.commit()
        except:
            messagebox.showerror(title="error", message="Email already used")
        conn.close()
        mycursor.close()
   

if __name__=='__main__':   
    regframe = Tk()  
    Driverregistration(regframe)         
    regframe.mainloop()