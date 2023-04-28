
from tkinter import* 
from tkinter import ttk
from PIL import ImageTk, Image
from tkinter import messagebox
from dashboard import CustomerDash
from DriverDash import Driverdach
import mysql.connector
import os

class Login:
    def __init__(self, mainframe):   

        self.mainframe = mainframe
        self.mainframe.geometry("800x500")
        self.mainframe.resizable(False,False)
        self.mainframe.configure(bg='#A6F47F')
        self.mainframe.title("Login")

        #frames

        rightframe = Frame(self.mainframe, bg = "white",  width = 450 , height=500)
        rightframe.pack(side=RIGHT)  

        #label/entry 
        titlelbl = Label(rightframe, bg = 'white', font= 30 , text="Login")
        titlelbl.place(x= 200, y= 40)

        Emaillbl = Label(rightframe, bg = 'white', text="Email")
        Emaillbl.place(x= 127, y= 140)

        self.Emailtxt = Entry(rightframe,width= 30, highlightthickness=1,  highlightbackground = "black", highlightcolor= "black")
        self.Emailtxt.place(x= 130, y= 160)

        passwordlbl = Label(rightframe, bg = 'white', text="Password")
        passwordlbl.place(x= 127, y= 190)

        self.passwordtxt = Entry(rightframe,width= 30, highlightthickness=1,  highlightbackground = "black", highlightcolor= "black",show="*")
        self.passwordtxt.place(x= 130, y= 210)

        #btn
        Login_btn = Button(rightframe,text="Login", width=10, command=self.admin)
        Login_btn.place(x = 180, y = 300)

        btn_reg = Button(rightframe,text="Create account", width=20,bg='white', borderwidth=0,relief=SUNKEN,activebackground='white',activeforeground='green',command= self.registerpage)
        btn_reg.place(x = 150, y = 260)

        lblDriver_reg = Label(rightframe, text="Do you wanna be a driver?", bg= "white")
        lblDriver_reg.place(x=10, y =480)

        btn_driver_reg = Button(rightframe,text="Click here", width=7,bg='white', borderwidth=0,relief=SUNKEN,activebackground='white',activeforeground='green', command= self.open_driverreg)
        btn_driver_reg.place(x = 154, y = 480)
        
        #combobox
        self.value = StringVar()
        self.usertypebox = ttk.Combobox(rightframe, width= 20, textvariable=self.value)
        self.usertypebox['values']=('Driver','Customer')   
        self.usertypebox.set("User type")
        self.usertypebox.place(x = 150, y =100)

        # insert img    
        img1 = Image.open("good-icon.png").resize((200,200))
        self.img = ImageTk.PhotoImage(img1)
        imglabel = Label(self.mainframe, image =self.img, bg ='#A6F47F')
        imglabel.place(x=70, y =130) 
          
    #user type from combox
    def on_select(self):
        self.user_type = str(self.value.get())
        
#admin check
    def admin(self):
        if self.Emailtxt.get() == "admin@gmail.com" and self.passwordtxt.get() == "admin":
            os.system('python admindash.py')
        else:
            self.usertype()
    #user type
    def usertype(self):
        self.on_select()
        if self.user_type  == "Driver":
            self.Driver_verification()
        elif self.user_type  =="Customer":
            self.verification()
        else:
            messagebox.showerror(title="error", message="select a user type")

    #send value to dashboard
    def dashboard_open(self, email):
        self.booking = Toplevel(self.mainframe)
        self.Dash_booking = CustomerDash(self.booking, email)

    def driver_dash_open(self, email):
        self.dash = Toplevel(self.mainframe)
        self.Dash_Driver = Driverdach(self.dash, email)
    

    #mysql connection
    def connect(self):
        conn = None
        try:
            conn = mysql.connector.connect(host='localhost', port=3306, user='root', password='', database='taxisystem')
            print("Connected!")
        except:
            print("Error: ", sys.exc_info())
        finally:
            return conn
            
    #email and password check from mysql
    def verification(self):
            conn = self.connect()
            mycursor = conn.cursor()
            global cid
            email = self.Emailtxt.get()
            insertquery = insertquery = "select Id, email, password from userinfo where email = %s and password = %s" 
            values = (self.Emailtxt.get(), self.passwordtxt.get())
            try:
                mycursor.execute(insertquery,values)
                cid= mycursor.fetchall()
                if cid[0] != "":   
                    self.dashboard_open(email)                                                      
                else:
                    messagebox.showerror(title="error", message="wrong email or password")
            except:
                messagebox.showerror(title="error", message="wrong email or password")
            conn.commit()
        
            conn.close()
            mycursor.close()

    def Driver_verification(self):
            conn = self.connect()
            mycursor = conn.cursor()
            global cid
            email = self.Emailtxt.get()
            insertquery = insertquery = "select DriverID, email, password from Driverinfo where email = %s and password = %s" 
            values = (self.Emailtxt.get(), self.passwordtxt.get())
            try:    
                mycursor.execute(insertquery,values)
                cid= mycursor.fetchall()
                if cid[0] != "":  
                    self.driver_dash_open(email)                                                      
                else:
                    messagebox.showerror(title="error", message="wrong email or password")
            except:
                messagebox.showerror(title="error", message="wrong email or password")
            conn.commit()
        
            conn.close()
            mycursor.close()

    def registerpage(self):
        os.system('python register.py')

    def open_driverreg(self):
        os.system('python DriverRegistration.py')

if __name__=='__main__':  
    mainframe = Tk()
    Login(mainframe)
    mainframe.mainloop() 


