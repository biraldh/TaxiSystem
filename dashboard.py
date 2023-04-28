from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
import mysql.connector
from tkcalendar import Calendar, DateEntry
import sys

import os

class CustomerDash:
    def __init__(self, dashframe, email):
        self.email = email
        self.dashframe = dashframe
        self.dashframe.geometry("1000x600")
        self.dashframe.resizable(False,False)  
        self.dashframe.title("User Dashboard")
        self.dashframe.config(bg='#6be2ed')
        #frame
        tab = Frame(self.dashframe, bg = '#A6F47F', width = 50 , height=600)
        tab.pack(side=LEFT)

        booking_table = Frame(self.dashframe,width=400, height=600, bg='#6be2ed')
        booking_table.pack(side=RIGHT)

        #entry/label
        timelbl = Label(self.dashframe, text="time of pickup", width =20,bg='#6be2ed')
        timelbl.place(x = 120, y = 160)

        self.timetxt = Entry(self.dashframe)
        self.timetxt.place(x = 130, y = 180)

        pickuplbl = Label(self.dashframe, text="Pickup point", width =20,bg='#6be2ed')
        pickuplbl.place(x = 120, y = 100)

        self.pickuptxt = Entry(self.dashframe)
        self.pickuptxt.place(x = 130, y = 120)

        Destinationlbl = Label(self.dashframe, text="Destination", width =20,bg='#6be2ed')
        Destinationlbl.place(x = 120, y = 50)

        self.Destinationtxt = Entry(self.dashframe)
        self.Destinationtxt.place(x = 130, y = 70)

        Datelbl = Label(self.dashframe, text="Date of pickup", width =20,bg='#6be2ed')
        Datelbl.place(x = 120, y = 220)

        self.Datetxt = DateEntry(self.dashframe, font=("Arail",13),bg="lightyellow",width=12, date_pattern='yyyy-MM-dd')
        self.Datetxt.place(x = 130, y = 240)    

        #buttons
        confirmbtn = Button(self.dashframe, text= "Confirm", width= 10, command = self.verifyall)
        confirmbtn.place(x= 150, y = 300)

        editbtn = Button(self.dashframe, text= "Update", width= 10, command = self.editbooking)
        editbtn.place(x= 150, y = 350)

        deletebtn = Button(self.dashframe, text= "Delete", width= 10, command = self.deletebooking)
        deletebtn.place(x= 150, y = 400)

        searchbtn = Button(self.dashframe, text="search", command= self.booking_view, width= 20)
        searchbtn.place(x= 400,y=150)

        #img
        exit_img = Image.open("exit.png").resize((30,30))
        self.exitimg = ImageTk.PhotoImage(exit_img)
        exitbtn = Button(tab, image =self.exitimg, bg='#A6F47F', borderwidth=0, relief=SUNKEN, activebackground='#82cc5e', command= self.exit)
        exitbtn.place(x=9,y=500)

        #combobox
        self.value = StringVar()
        self.status = ttk.Combobox(self.dashframe, width= 20, textvariable=self.value)
        self.status['values']=('Confirmed','unconfirmed')   
        self.status.set("booking Status")
        self.status.place(x = 600, y =150)

        #booking view
        scroll = Scrollbar(booking_table,orient= VERTICAL)
        scroll.pack(side=RIGHT, fill=Y)

        self.booking_list = ttk.Treeview(booking_table, columns=("BookingID", "pickup_date", "pickup_time", "Destination", "Pickup_location", "Booking_status", "DriverId"), xscrollcommand = scroll.set)
        
        #columns
        self.booking_list.column("BookingID", width = 70)
        self.booking_list.column("pickup_date", width = 90)
        self.booking_list.column("pickup_time", width = 90)
        self.booking_list.column("Destination", width = 90)
        self.booking_list.column("Pickup_location", width = 90)
        self.booking_list.column("Booking_status", width = 90)
        self.booking_list.column("DriverId", width = 80)
        #header 
        self.booking_list.heading("BookingID", text = "Booking Id")
        self.booking_list.heading("pickup_date",text="Pickup Date")
        self.booking_list.heading("pickup_time",text = "Pickup time")
        self.booking_list.heading("Destination",text ="Destination")
        self.booking_list.heading("Pickup_location",text = "Pickup location")
        self.booking_list.heading("Booking_status",text = "booking status")
        self.booking_list.heading("DriverId",text = "Driver ID")

        self.booking_list.bind('<ButtonRelease-1>', self.selectItem)
        self.booking_list['show'] = 'headings'

        self.booking_list.pack(fill = BOTH, expand = 1, padx=20)
    
    #combobox select value
    def on_select(self):
        self.booking_status = str(self.value.get())

    #select value from table
    def selectItem(self,value):
        self.cleartext()
        curItem = self.booking_list.focus()
        table_value=self.booking_list.item(curItem)
        rows = table_value['values']
        self.booking_id = rows[0]
        self.pick_up_date= rows[1]
        self.Datetxt.insert(0, self.pick_up_date)
        self.pick_up_time = rows[2]
        self.timetxt.insert(0,self.pick_up_time)
        self.destination = rows[3]
        self.Destinationtxt.insert(0,self.destination)
        self.pick_up_location = rows[4]
        self.pickuptxt.insert(0,self.pick_up_location)

        
    #clearing text in entry field
    def cleartext(self):
        self.timetxt.delete(0,END)
        self.Destinationtxt.delete(0,END)
        self.pickuptxt.delete(0,END)
        self.Datetxt.delete(0,END)

    def verifyall(self):
        if self.Datetxt.get() !="" and self.Destinationtxt.get() !="" and self.pickuptxt.get() != "" and self.timetxt.get() != "":
            self.bookingrequest()
        else:
            messagebox.showerror(title="error", message="fill all the fields")
         

    #connection
    def connect(self): 
        conn = None
        try:
            conn = mysql.connector.connect(host='localhost', port=3306, user='root', password='', database='taxisystem')
            print("Connected!")
        except:
            print("Error: ", sys.exc_info())
        finally:
            return conn

    #fillbookingtable
    def booking_view(self):
        self.on_select()
        conn = self.connect()
        mycursor = conn.cursor()
        book_status = self.booking_status
        
        try:
        #getting userid
            user_id = mycursor.execute("select Id from userinfo where email = '%s'" %(self.email))
            mycursor.execute(user_id)
            user_id = mycursor.fetchone()[0]
        except Exception as e:
            messagebox.showerror("Error",f"Due to {str(e)}",parent=self.dashframe)
        values=(user_id, book_status)
        query="select BookingID, pickup_date, pickup_time, Destination, Pickup_location, Booking_status, DriverId from booking where UserinfoID =%s and Booking_status = %s"
        try:   
            mycursor.execute(query, values)
            booking_data = mycursor.fetchall()
            for i in self.booking_list.get_children():
                self.booking_list.delete(i)
            for row in booking_data:
                self.booking_list.insert("", END,values = row)
            
        except Exception as e:
            messagebox.showerror("Error",f"Due to {str(e)}",parent=self.dashframe)
        conn.commit()
        conn.close()

    #booking   
    def bookingrequest(self):
    
        conn = self.connect()
        mycursor = conn.cursor()
        try:
        #getting userid
            user_id = mycursor.execute("select Id from userinfo where email = '%s'" %(self.email))
            mycursor.execute(user_id)
            user_id = mycursor.fetchone()[0]
        except Exception as e:
            messagebox.showerror("Error",f"Due to {str(e)}",parent=self.dashframe)
        try:
            values = ( self.Datetxt.get(), self.timetxt.get(),self.Destinationtxt.get(), self.pickuptxt.get(),user_id,"Pending", "unconfirmed")
            query ="insert into Booking (pickup_date, pickup_time, Destination, Pickup_location, UserinfoID, payment, Booking_status) values (%s,%s,%s,%s,%s,%s,%s)"
            mycursor.execute(query,values)
            messagebox.showinfo(title="Requested", message="Request for ride sent")
        except Exception as e:
            messagebox.showerror("Error",f"Due to {str(e)}",parent=self.dashframe)
        conn.commit()
        conn.close()

    #editbooking
    def editbooking(self):
        conn = self.connect()
        mycursor = conn.cursor()
        try:
            values = ( self.Datetxt.get(), self.timetxt.get(),self.Destinationtxt.get(), self.pickuptxt.get(),self.booking_id)
            query="update booking set pickup_date =%s, pickup_time=%s, Destination=%s, Pickup_location=%s where BookingID = %s"
            mycursor.execute(query,values)
            messagebox.showinfo(title="Updated", message="Booking updated")
        except Exception as e:
            messagebox.showerror("Error",f"Due to {str(e)}",parent=self.dashframe)
        conn.commit()
        conn.close()

    #delete booking
    def deletebooking(self):
        conn = self.connect()
        mycursor = conn.cursor()
        try:
            mycursor.execute("delete from booking where BookingID = '%s'"%(self.booking_id))
            messagebox.showinfo(title="Requested", message="Booking deleted")
        except Exception as e:
            messagebox.showerror("Error",f"Due to {str(e)}",parent=self.dashframe)
        conn.commit()
        conn.close()
    
    def exit(self):
        sys.exit()
if __name__=='__main__':          
    dashframe = Tk()
    CustomerDash(dashframe)
    dashframe.mainloop()
    