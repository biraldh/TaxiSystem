from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
from tkinter import ttk
import sys
import mysql.connector
from tkinter import messagebox
import re

class registration():
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

        self.addresstxt = Entry(rightframe,width= 30)
        self.addresstxt.place(x= 480, y= 320)

        #button
        # btn_back = Button(rightframe,text="Login page", width=20,bg='white', borderwidth=0,relief=SUNKEN,activebackground='white',activeforeground='green',command= self.registerpage)
        # btn_back.place(x = 150, y = 500)

        Register_btn = Button(rightframe,text="Register", width=10, command = self.validation)
        Register_btn.place(x = 540, y = 370)

        img1 = Image.open("customerregimg.jpg").resize((400,500))
        self.img = ImageTk.PhotoImage(img1)
        imglabel = Label(regframe, image =self.img)
        imglabel.place(x=0, y =0)

        #combobox
        self.value = StringVar()
        self.paytypebox = ttk.Combobox(rightframe, width= 27, textvariable=self.value)
        self.paytypebox['values']=('Credit Card','Cash','Online payment')   
        self.paytypebox.set("Payment Method")
        self.paytypebox.place(x = 480, y =80)
    
    def on_select(self):
        self.pay_type = str(self.value.get())

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
        nameval = self.usernametxt.get()
        emailval = self.Emailtxt.get()
        passval = self.passwordtxt.get()
        phoneval = self.Phonenumtxt.get()
        addressval = self.addresstxt.get() 

        if nameval =="" or emailval == "" or passval == "" or phoneval == "" or addressval == "":
            messagebox.showerror(title="error", message="fill all the fields")
            
        else:
            if re.match(pat, emailval):
                self.sendtodatabase()
            else : 
                messagebox.showerror(title="error", message="Invalid email") 
                
    def sendtodatabase(self):
        self.on_select()
        self.namemid = self.usernametxt.get()
        self.emailmid = self.Emailtxt.get()
        self.passmid = self.passwordtxt.get()
        self.phonemid = self.Phonenumtxt.get()
        self.addressmid = self.addresstxt.get() 

        conn = self.connect()
        mycursor = conn.cursor()
        try:
            insertquery = "INSERT INTO userinfo (name, email,phone_num,password, address,payment_method) VALUES (%s, %s, %s, %s, %s, %s)"
            values = (self.namemid,self.emailmid, self.phonemid, self.passmid, self.addressmid, self.pay_type)
            mycursor.execute(insertquery,values)
            messagebox.showinfo(title="Registered", message="Registration successfully done")
            conn.commit()
        except:
            messagebox.showerror(title="error", message="Email already used")
        conn.close()
        mycursor.close()
  

if __name__=='__main__':   
    regframe = Tk()  
    registration(regframe)         
    regframe.mainloop()