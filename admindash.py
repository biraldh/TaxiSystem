from tkinter import *
from tkinter import ttk
import mysql.connector
from tkinter import messagebox
from PIL import Image, ImageTk
import sys
class Admindash():
    def __init__(self, adminframe):
        self.adminframe = adminframe
        self.adminframe.title("Admin Dashboard")
        self.adminframe.geometry("1000x600")

        #frames
        self.tab =Frame(self.adminframe, width=50, bg = "red")
        self.tab.pack(fill=Y, side= LEFT)

        self.center = Frame(self.adminframe, width=500, bg= "green")
        self.center.pack(fill=Y, side= RIGHT)

        #label and combobox/entry
        Booking_id_lbl = Label(self.adminframe, text= "Booking ID", font= 20)
        Booking_id_lbl.place(x= 150, y =100)

        self.booking_id_entry = Entry(self.adminframe, highlightthickness=1,  highlightbackground = "black", highlightcolor= "black")
        self.booking_id_entry.place(x = 150, y =150)

        Driver_id_lbl = Label(self.adminframe, text= "Available Drivers", font= 20)
        Driver_id_lbl.place(x= 150, y =200)

        self.drivervalue = StringVar()
        self.driver_id_box =  ttk.Combobox(self.adminframe, width= 20, textvariable=self.drivervalue)  
        self.driver_id_box.place(x = 150, y =250)

        #button
        confirmbtn = Button(self.adminframe, width= 20, text="Assign Driver", command= self.Assign_driver)
        confirmbtn.place(x= 150, y = 300)

        searchbtn = Button(self.adminframe, text="Search records", command= self.customer_booking_view)
        searchbtn.place(x= 300, y = 10)
        
        exit_img = Image.open("exit.png").resize((30,30))
        self.exitimg = ImageTk.PhotoImage(exit_img)
        exitbtn = Button(self.adminframe, image =self.exitimg, bg='red', borderwidth=0, relief=SUNKEN, activebackground='#d12a4e', command= self.exit)
        exitbtn.place(x=9,y=500)

        self.driver_data()

        #combobox
        self.value = StringVar()
        self.status = ttk.Combobox(self.adminframe, textvariable=self.value)
        self.status['values']=('Confirmed','unconfirmed','Completed')   
        self.status.set("booking Status")
        self.status.place(x = 245, y =50)


        #table
        scrollwhel = Scrollbar(self.center,orient= VERTICAL)
        scrollwhel.pack(side=RIGHT, fill=Y)

        self.booking_table = ttk.Treeview(self.center, columns=("BookingID", "pickup_date", "pickup_time", "Destination", "Pickup_location", "Booking_status","userid"),xscrollcommand = scrollwhel.set)
        #columns
        self.booking_table.column("BookingID", width = 70)
        self.booking_table.column("pickup_date", width = 90)
        self.booking_table.column("pickup_time", width = 90)
        self.booking_table.column("Destination", width = 90)
        self.booking_table.column("Pickup_location", width = 90)
        self.booking_table.column("Booking_status", width = 90)
        self.booking_table.column("userid", width = 70)
        #header 
        self.booking_table.heading("BookingID", text = "Booking Id")
        self.booking_table.heading("pickup_date",text="Pickup Date")
        self.booking_table.heading("pickup_time",text = "Pickup time")
        self.booking_table.heading("Destination",text ="Destination")
        self.booking_table.heading("Pickup_location",text = "Pickup location")
        self.booking_table.heading("Booking_status",text = "booking status")
        self.booking_table.heading("userid",text = "User ID")
        self.booking_table['show'] = 'headings'
        self.booking_table.pack(fill= BOTH, expand= 1)
        self.booking_table.bind('<ButtonRelease-1>', self.selectItem)

    def selectItem(self,value):
        self.cleartext()
        curItem = self.booking_table.focus()
        table_value=self.booking_table.item(curItem)
        rows = table_value['values']
        self.booking_id = rows[0]
        self.booking_id_entry.insert(0, self.booking_id)
    
    #combobox selected item for table
    def on_select(self):
        self.booking_status = str(self.value.get())
      
    #clearing text in entry field
    def cleartext(self):
        self.booking_id_entry.delete(0,END)

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
    
    #fill the tree view
    def customer_booking_view(self):
            conn = self.connect()
            mycursor = conn.cursor()
            self.on_select()
            value = self.booking_status      
            mycursor.execute("select BookingID, pickup_date, pickup_time, Destination, Pickup_location, Booking_status, UserinfoID from Booking WHERE Booking_status='%s'" %(value))
            booking_data = mycursor.fetchall()
            for i in self.booking_table.get_children():
                self.booking_table.delete(i)
            for row in booking_data:
                self.booking_table.insert("", END,values = row)
            # for row in booking_data:
            #     self.booking_table.insert("", "end", text=row[0], values=(row[1], row[2], row[3],row[4], row[5], row[6], row[7]))
            conn.commit()
            conn.close()

    #driver id for combobox
    def driver_data(self):
        conn = self.connect()
        mycursor = conn.cursor() 
        try:
            query ="select DriverID from Driverinfo where Driver_status = '%s'" %("Available")
            mycursor.execute(query)
            driver_id = mycursor.fetchall()
            value =[row[0] for row in driver_id]
            self.driver_id_box.configure(values=value)
        except Exception as e:
            messagebox.showerror("Error",f"Due to {str(e)}",parent=self.adminframe)
            
    #assign driver to booking/change status
    def Assign_driver(self):
        book_id = self.booking_id_entry.get()
        drive_id = self.drivervalue.get()
        conn = self.connect()
        mycursor = conn.cursor()
        values = (drive_id,"Confirmed", book_id)
        values_status=("Uavailable", drive_id)
        query = "update booking set DriverId = %s, Booking_status = %s where BookingID = %s"
        query_status = "update Driverinfo set Driver_status = %s where DriverID = %s"
        try:
            mycursor.execute(query,values)
            mycursor.execute(query_status,values_status)
            messagebox.showinfo(title="Completed", message="A driver has been assigned")
        except Exception as e:
            messagebox.showerror("Error",f"Due to {str(e)}",parent=self.adminframe)   
        conn.commit()
        conn.close()

    
    def exit(self):
        sys.exit()

if __name__=='__main__':   
    adminframe = Tk()  
    Admindash(adminframe)         
    adminframe.mainloop()