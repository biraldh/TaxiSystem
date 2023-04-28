from tkinter import *
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter import messagebox
import datetime
from tkcalendar import Calendar, DateEntry
import mysql.connector
class Booking:
  def __init__(self,book,email):      #initialization
    self.book = book
    self.book.title("Trip Booking")
    self.book.geometry("1400x700+0+0")
    self.book.state("zoomed")
    self.book.config(bg="white")

  # -------------text_variables-----------------------------------------------------------
    self.var_booking_id = IntVar()
    self.var_pickup_place = StringVar()
    self.var_dropoff_place = StringVar()
    self.var_pickup_date = StringVar()
    self.var_dropoff_date = StringVar()
    self.var_pickup_time = StringVar()
    self.var_dropoff_time = StringVar()
    self.var_user_id= StringVar()
    self.email= email

    # --------------------------------------------------------------------------------------------------
    # initialize frame1
    frame_1 = Frame(self.book,bg='black')
    frame_1.place(x=0 , y=0, width = 590, height=700)

    my_bg = Image.open(r'C:\Users\asus\Desktop\book_taxi\book_trip.png').resize((590,700))
    self.bg = ImageTk.PhotoImage(my_bg)
    lbl_bg = Label(frame_1, image= self.bg)
    lbl_bg.place(x=0,y=0,relwidth=1,relheight=1)
    # -------------------------------------------------------------------------------

    # frame for entry fields and buttons
    frame_2 = Frame(self.book,bg='white')
    frame_2.place(x=590 , y=0, width = 690, height=270)

    # frame for tree view
    frame_4 = Frame(self.book,bg='grey')
    frame_4.place(x=590 , y=270, width = 690, height=380)

    # --------labels-------------------------------
    lbl_pickup_place = Label(frame_2,text='Pickup Address',font=('Arial',13,'bold'),fg='black',bg='white')
    lbl_pickup_place.place(x=15,y=30)

    self.entry_pickup_place = Entry(frame_2, textvariable=self.var_pickup_place, width=24,font=('Arial',11,'bold'),border=1,bg="lightyellow")
    self.entry_pickup_place.place(x=15,y=60)

    lbl_dropoff_place = Label(frame_2,text='Dropoff Address',font=('Arial',13,'bold'),fg='black',bg='white')
    lbl_dropoff_place.place(x=265,y=30)

    self.entry_dropoff_place = Entry(frame_2, textvariable=self.var_dropoff_place, width=24,font=('Arial',11,'bold'),border=1,bg="lightyellow")
    self.entry_dropoff_place.place(x=265,y=60)

    lbl_pickup_date = Label(frame_2,text='Pickup Date',font=('Arial',13,'bold'),fg='black',bg='white')
    lbl_pickup_date.place(x=15,y=100) 

    self.entry_pickup_date=DateEntry(frame_2, textvariable=self.var_pickup_date, font=("Arail",13),bg="lightyellow",width=19)
    self.entry_pickup_date.place(x=15, y=130)

    lbl_dropoffdate = Label(frame_2,text='Dropoff Date',font=('Arial',13,'bold'),fg='black',bg='white')
    lbl_dropoffdate.place(x=265,y=100) 

    self.entry_dropoff_date=DateEntry(frame_2, textvariable=self.var_dropoff_date, font=("Arail",13),bg="lightyellow",width=19)
    self.entry_dropoff_date.place(x=265, y=130)

    lbl_pickup_time = Label(frame_2,text='Pickup Time',font=('Arial',13,'bold'),fg='black',bg='white')
    lbl_pickup_time.place(x=15,y=175) 

    self.entry_pickup_time = Entry(frame_2, textvariable=self.var_pickup_time, width=24,font=('Arial',11,'bold'),border=1,bg="lightyellow")
    self.entry_pickup_time.place(x=15,y=205)

    lbl_dropoff_time = Label(frame_2,text='Drop off Time',font=('Arial',13,'bold'),fg='black',bg='white')
    lbl_dropoff_time.place(x=265,y=176) 

    self.entry_dropff_time = Entry(frame_2, textvariable=self.var_dropoff_time, width=24,font=('Arial',11,'bold'),border=1,bg="lightyellow")
    self.entry_dropff_time.place(x=265,y=205)

    # ---------------Buttons-------------------------------

    btn_view = Button(frame_2,text='View',font=('Arial',13,'bold'),fg='black',bg='#6EB9DC',border=0,width=12,height=2,activebackground='#6EB9DC',activeforeground='black',cursor='hand2',command=self.display_data)
    btn_view.place(x=535,y=25)

    btn_book = Button(frame_2,text='ADD',font=('Arial',13,'bold'),fg='black',bg='#6EB9DC',border=0,width=12,height=2,activebackground='#6EB9DC',activeforeground='black',cursor='hand2',command=self.add_data)
    btn_book.place(x=535,y=80)

    btn_update = Button(frame_2,text='UPDATE',font=('Arial',13,'bold'),fg='black',bg='#6EB9DC',border=0,width=12,height=2,activebackground='#6EB9DC',activeforeground='black',cursor='hand2',command=self.update_data)
    btn_update.place(x=535,y=135)

    btn_delete = Button(frame_2,text='DELETE',font=('Arial',13,'bold'),fg='black',bg='#6EB9DC',border=0,width=12,height=2,activebackground='#6EB9DC',activeforeground='black',cursor='hand2',command=self.delete_data)
    btn_delete.place(x=535,y=190)

    # ------------scrollbar and treeview--------------------------------
    scroll_win = Scrollbar(frame_4,orient= VERTICAL)

    self.tr_booking = ttk.Treeview(frame_4,height=15,columns=("booking_id","pickup_address","dropoff_address","pickup_date","dropoff_date","pickup_time","dropoff_time","booking_status","user_id"),xscrollcommand = scroll_win.set)
    scroll_win.pack(side=RIGHT, fill=Y)

    self.tr_booking.heading("booking_id",text= "booking_id")
    self.tr_booking.heading("pickup_address",text= "pickup_address")
    self.tr_booking.heading("dropoff_address",text= "dropoff_address")
    self.tr_booking.heading("pickup_date",text= "pickup_date")
    self.tr_booking.heading("dropoff_date",text= "dropoff_date")
    self.tr_booking.heading("pickup_time",text= "pickup_time")
    self.tr_booking.heading("dropoff_time",text= "dropoff_time")
    self.tr_booking.heading("booking_status",text= "booking_status")
    self.tr_booking.heading("user_id",text= "user_id")

    self.tr_booking['show'] = 'headings'

    self.tr_booking.column("booking_id",width = 100)
    self.tr_booking.column("pickup_address",width = 110)
    self.tr_booking.column("dropoff_address",width = 110)
    self.tr_booking.column("pickup_date",width = 110)
    self.tr_booking.column("dropoff_date",width = 110)
    self.tr_booking.column("pickup_time",width = 110)
    self.tr_booking.column("dropoff_time",width = 110)
    self.tr_booking.column("booking_status",width = 110)
    self.tr_booking.column("user_id",width = 110)

    self.tr_booking.pack(fill=BOTH, expand=1)
    self.tr_booking.bind("<ButtonRelease-1>",self.tree_click)

# -----------------functions-----------------------------------------
  # connect_database function
  def connection(self):
    conn = mysql.connector.connect(host = 'localhost', user ='root',password ='Phurwa@807',database = 'pcps_python')
    return conn

  # treeview click data function
  def tree_click(self,event):
    data_view = self.tr_booking.focus()
    click_tree = self.tr_booking.item(data_view)
    row = click_tree['values']
    self.var_booking_id.set(row[0])
    self.var_pickup_place.set(row[1]),
    self.var_dropoff_place.set(row[2]),
    self.var_pickup_date.set(row[3]),
    self.var_dropoff_date.set(row[4]),
    self.var_pickup_time.set(row[5]),
    self.var_dropoff_time.set(row[6]), 
# -----------------------------------------------------------------
  
  # add new data
  def add_data(self):
    print(self.email)
    if self.var_pickup_place.get() == "":
      messagebox.showerror("Error", "Please Enter Pickup Address",parent=self.book)
    elif self.var_dropoff_place.get() == "":
      messagebox.showerror("Error", "Please Enter Drop off Address",parent=self.book)
    elif self.var_pickup_date.get() == "":
      messagebox.showerror("Error", "Please Enter Pickup Date",parent=self.book)
    elif self.var_dropoff_date.get() == "":
      messagebox.showerror("Error", "Please Enter Drop off Date",parent=self.book)
    elif self.var_pickup_time.get() == "":
      messagebox.showerror("Error", "Please Enter Pick up Time",parent=self.book)
    elif self.var_dropoff_time.get() == "":
      messagebox.showerror("Error", "Please Enter Drop off Time",parent=self.book)
    else:
      try:
        conn = self.connection()
        my_cursor = conn.cursor()
        user_id = my_cursor.execute("select user_id from user where email = '%s'" %(self.email))
        my_cursor.execute(user_id)
        cu_id = my_cursor.fetchone()[0]
        my_cursor.execute('insert into booking values(%s,%s,%s,%s,%s,%s,%s,%s,%s)',(
                                                                      self.var_booking_id.get(),
                                                                      self.var_pickup_place.get(),
                                                                      self.var_dropoff_place.get(),
                                                                      self.var_pickup_date.get(),
                                                                      self.var_dropoff_date.get(),
                                                                      self.var_pickup_time.get(),
                                                                      self.var_dropoff_time.get(),
                                                                      'Pending',
                                                                      cu_id,                                                                
                                                                                ))      
        conn.commit()
        conn.close()
        messagebox.showinfo('Success','Booking Successfull',parent=self.book)
        self.reset()    #clear the fields
        self.display_data()
      except Exception as e:
        messagebox.showerror("Error",f"Due to {str(e)}",parent=self.book)
# ----------------------------------------------------------------------------------------
  # display in treeview
  def display_data(self):
    try:
      conn = self.connection()
      my_cursor = conn.cursor()
      u_id = my_cursor.execute("select user_id from user where email = '%s'" %(self.email))
      my_cursor.execute(u_id)
      u_id = my_cursor.fetchone()[0]
      my_cursor.execute("select * from booking where booking_status = 'Pending' and user_id ='%s'"%(u_id))
      book_data= my_cursor.fetchall()
      if len(book_data) != 0:
        self.tr_booking.delete(*self.tr_booking.get_children())
        for row in book_data:
          self.tr_booking.insert("", END,values = row)

      conn.commit()
      conn.close()

    except Exception as e:
        messagebox.showerror("Error",f"Due to {str(e)}",parent=self.book)
      
# ------------------------------------------------------------------------------------
  # update the booking_data
  def update_data(self):
    try:
      conn = self.connection()
      my_cursor = conn.cursor(buffered=True)
      my_cursor.execute("update booking set pickup_address = %s,dropoff_address = %s,pickup_date = %s,dropoff_date=%s,pickup_time=%s,dropoff_time=%s where booking_id = %s",(
        self.var_pickup_place.get(),
        self.var_dropoff_place.get(),
        self.var_pickup_date.get(),
        self.var_dropoff_date.get(),
        self.var_pickup_time.get(),
        self.var_dropoff_time.get(),
        self.var_booking_id.get()
                                                                                                                ))
      conn.commit()
      conn.close()
      messagebox.showinfo('Success','updated Successfull',parent=self.book)
      self.reset()    #clear the fields
      self.display_data()
    except Exception as e:
      messagebox.showerror("Error",f"Due to {str(e)}",parent=self.book)
# ----------------------------------------------------------------------------------
  # delete data
  def delete_data(self):
    try:
        conn = self.connection()
        my_cursor = conn.cursor(buffered=True)
        my_cursor.execute("delete from booking where booking_id = %s",(
          self.var_booking_id.get(),
        ))
        conn.commit()
        conn.close()
        messagebox.showinfo("Message","Data Deleted",parent=self.book)
        self.reset()    #clear the fields
        self.display_data()
    except Exception as e:
        messagebox.showerror("Error",f"Due to {str(e)}",parent=self.book)
# --------------------------------------------------
  # reset funtion to clear fields
  def reset(self):
      self.var_pickup_place.set('')
      self.var_dropoff_place.set('')
      self.var_pickup_date.set('')
      self.var_dropoff_date.set('')
      self.var_pickup_time.set('')
      self.var_dropoff_time.set('')


# main function
if __name__ == '_main_':
  book = Tk()
  bb = Booking(book)
  book.mainloop()