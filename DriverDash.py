from tkinter import *
from tkinter import ttk
import mysql.connector
from tkinter import messagebox
import sys
from PIL import Image, ImageTk
class Driverdach():
    def __init__(self,Driverframe,email ):
        self.email = email
        self.Driverframe = Driverframe
        self.Driverframe.geometry("1000x600")
        self.Driverframe.resizable(False,False)
        self.Driverframe.title("Driver Dashboard")
        self.Driverframe.configure(bg = "#52eb7b")
        #frames
        tableframe = Frame(self.Driverframe)
        tableframe.configure(bg = "#d2d494")
        tableframe.pack(side=RIGHT)

        tab = Frame(self.Driverframe, bg = 'white', width = 50 , height=600)
        tab.pack(side=LEFT)

        #label
        bookinglbl = Label(self.Driverframe, text= "Booking ID : ",bg = "#52eb7b")
        bookinglbl.place(x =50, y = 150)

        self.bookinglbl_confirm = Label(self.Driverframe,bg = "#52eb7b")
        self.bookinglbl_confirm.place(x = 150, y =150)

        pick_up_lbl = Label(self.Driverframe, text= "Pick up location : ",bg = "#52eb7b")
        pick_up_lbl.place(x =50, y = 180)

        self.pick_up_confirm = Label(self.Driverframe,bg = "#52eb7b")
        self.pick_up_confirm.place(x = 150, y =180)

        destination_lbl = Label(self.Driverframe, text= "Destination : ",bg = "#52eb7b")
        destination_lbl.place(x =50, y = 210)

        self.destination_confirm = Label(self.Driverframe,bg = "#52eb7b")
        self.destination_confirm.place(x = 150, y =210)

        #button
        searchbtn = Button(self.Driverframe, text="Search",command= self.booking_view)
        searchbtn.place(x = 370, y =150)

        completebtn = Button(self.Driverframe, text="Completed", command= self.trip_complete)
        completebtn.place(x= 50, y =250)

        exit_img = Image.open("exit.png").resize((30,30))
        self.exitimg = ImageTk.PhotoImage(exit_img)
        exitbtn = Button(tab, image =self.exitimg, bg='white', borderwidth=0, relief=SUNKEN, activebackground='gray', command= self.exit)
        exitbtn.place(x=9,y=500)

        #combobox
        self.value = StringVar()
        self.status = ttk.Combobox(self.Driverframe, width= 20, textvariable=self.value)
        self.status['values']=('Confirmed','Completed')   
        self.status.set("booking Status")
        self.status.place(x = 600, y =150)
        
        #table
        scroll = Scrollbar(tableframe ,orient= VERTICAL)
        scroll.pack(side=RIGHT, fill=Y)

        self.list_booking = ttk.Treeview(tableframe , columns=("BookingID", "pickup_date", "pickup_time", "Destination", "Pickup_location", "Booking_status", "customerId"), xscrollcommand = scroll.set)
        
        #columns
        self.list_booking.column("BookingID", width = 70)
        self.list_booking.column("pickup_date", width = 90)
        self.list_booking.column("pickup_time", width = 90)
        self.list_booking.column("Destination", width = 90)
        self.list_booking.column("Pickup_location", width = 90)
        self.list_booking.column("Booking_status", width = 90)
        self.list_booking.column("customerId", width = 80)
        #header 
        self.list_booking.heading("BookingID", text = "Booking Id")
        self.list_booking.heading("pickup_date",text="Pickup Date")
        self.list_booking.heading("pickup_time",text = "Pickup time")
        self.list_booking.heading("Destination",text ="Destination")
        self.list_booking.heading("Pickup_location",text = "Pickup location")
        self.list_booking.heading("Booking_status",text = "booking status")
        self.list_booking.heading("customerId",text = "Customer ID")

        self.list_booking['show'] = 'headings'
        
        self.list_booking.bind('<ButtonRelease-1>', self.selectItem)

        self.list_booking.pack(fill = BOTH, expand = 1, padx=20)

    #combobox selected item
    def on_select(self):
        self.booking_status = str(self.value.get())

    #table selected item
    def selectItem(self,value):
        self.cleartext()
        curItem = self.list_booking.focus()
        table_value=self.list_booking.item(curItem)
        rows = table_value['values']
        self.booking_id = rows[0]
        self.bookinglbl_confirm.config(text=self.booking_id)
        self.pick_up_location = rows[4]
        self.pick_up_confirm.config(text=self.pick_up_location)
        self.destination = rows[3]
        self.destination_confirm.config(text=self.destination)
    
    def cleartext(self):
        self.bookinglbl_confirm.config(text="")
        self.pick_up_confirm.config(text="")
        self.destination_confirm.config(text="")
        
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
        conn = self.connect()
        mycursor = conn.cursor()
        self.on_select()
        try:
        #getting userid
            user_id = mycursor.execute("select DriverID from Driverinfo where email = '%s'" %(self.email))
            mycursor.execute(user_id)
            user_id = mycursor.fetchone()[0]
            self.driver_id = user_id
            values = (self.driver_id,self.booking_status)
            query="select BookingID, pickup_date, pickup_time, Destination, Pickup_location, Booking_status, UserinfoID from booking where DriverId =%s and Booking_status = %s"
        except Exception as e:
            messagebox.showerror("Error",f"Due to {str(e)}",parent=self.Driverframe)
        try:
            mycursor.execute(query, values)
            booking_data = mycursor.fetchall()
            for i in self.list_booking.get_children():
                self.list_booking.delete(i)
            for row in booking_data:
                self.list_booking.insert("", END,values = row)
            
        except Exception as e:
            messagebox.showerror("Error",f"Due to {str(e)}",parent=self.Driverframe)
        conn.commit()
        conn.close()

    #completed in bookingstatus
    def trip_complete(self):
        conn = self.connect()
        mycursor = conn.cursor()
        value_driver_status =("Available",self.driver_id)
        query_driver = "update Driverinfo set Driver_status = %s where DriverID = %s"
        value_booking = ("Completed", self.booking_id, self.driver_id)
        query_booking ="update booking set Booking_status = %s where BookingID = %s and DriverId = %s"
        try:
            mycursor.execute(query_driver, value_driver_status)
            mycursor.execute(query_booking, value_booking)
            messagebox.showinfo(title="Success", message="Ride has been completed")
        except Exception as e:
            messagebox.showerror("Error",f"Due to {str(e)}",parent=self.Driverframe)
        conn.commit()
        conn.close()

    #logout
    def exit(self):
        sys.exit()

if __name__=='__main__': 
    Driverframe = Tk()
    Driverdach(Driverframe)
    Driverframe.mainloop()