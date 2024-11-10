from tkinter import*
from PIL import Image,ImageTk
from tkinter import ttk,messagebox
import sqlite3
import os

class Register:
    def __init__(self,root):
        self.root=root
        self.root.title("Registration Window")
        self.root.geometry("1350x7000+0+0")
        self.root.config(bg="white")

        #-------Bg Image--------------
        self.bg=ImageTk.PhotoImage(file="bg_image.jpg")
        bg=Label(self.root,image=self.bg).place(x=250,y=0,relwidth=1,relheight=1)

        #-------left side Image--------------
        self.left=ImageTk.PhotoImage(file="side.jpg")
        left=Label(self.root,image=self.left).place(x=80,y=100,width=400,height=500)

        #-------register frame---------------
        frame1=Frame(self.root,bg="white")
        frame1.place(x=480,y=100,width=700,height=500)

        title=Label(frame1,text="REGISTER HERE",font=("times new roman",20,"bold"),bg="white",fg="blue").place(x=50,y=30)

        #-----------row1-------------------
        #self.var_fname=StringVar()
        f_name=Label(frame1,text="First Name",font=("times new roman",15,"bold"),bg="white",fg="black").place(x=50,y=100)
        self.txt_f_name=Entry(frame1,font=("times new roman",15),bg="lightyellow")
        self.txt_f_name.place(x=50,y=130,width=250)

        l_name=Label(frame1,text="Last Name",font=("times new roman",15,"bold"),bg="white",fg="black").place(x=370,y=100)
        self.txt_l_name=Entry(frame1,font=("times new roman",15),bg="lightyellow")
        self.txt_l_name.place(x=370,y=130,width=250)

        #-------------------row2-----------------------
        contact=Label(frame1,text="Contact No.",font=("times new roman",15,"bold"),bg="white",fg="black").place(x=50,y=170)
        self.txt_contact=Entry(frame1,font=("times new roman",15),bg="lightyellow")
        self.txt_contact.place(x=50,y=200,width=250)

        email=Label(frame1,text="Email",font=("times new roman",15,"bold"),bg="white",fg="black").place(x=370,y=170)
        self.txt_email=Entry(frame1,font=("times new roman",15),bg="lightyellow")
        self.txt_email.place(x=370,y=200,width=250)

        #----------------row3-------------------
        question=Label(frame1,text="Security Question",font=("times new roman",15,"bold"),bg="white",fg="black").place(x=50,y=240)
        self.cmb_quest=ttk.Combobox(frame1,font=("times new roman",13),state='readonly',justify=CENTER)
        self.cmb_quest['values']=("Select","Your First Pet Name","Your Birth Place","Your Best Friend Name")
        self.cmb_quest.place(x=50,y=270,width=250)
        self.cmb_quest.current(0)

        answer=Label(frame1,text="Answer",font=("times new roman",15,"bold"),bg="white",fg="black").place(x=370,y=240)
        self.txt_answer=Entry(frame1,font=("times new roman",15),bg="lightyellow")
        self.txt_answer.place(x=370,y=270,width=250)

        #-------------------row4-----------------------
        password=Label(frame1,text="Password",font=("times new roman",15,"bold"),bg="white",fg="black").place(x=50,y=310)
        self.txt_password=Entry(frame1,font=("times new roman",15),bg="lightyellow")
        self.txt_password.place(x=50,y=340,width=250)

        cnf_password=Label(frame1,text="Confirm Password",font=("times new roman",15,"bold"),bg="white",fg="black").place(x=370,y=310)
        self.txt_cnf_password=Entry(frame1,font=("times new roman",15),bg="lightyellow")
        self.txt_cnf_password.place(x=370,y=340,width=250)

        #----------checkbox--------------------
        self.var_chk=IntVar()
        chk=Checkbutton(frame1,text="I Agree The Terms & Conditions",variable=self.var_chk,onvalue=1,offvalue=0,font=("times new roman",12),bg="lightblue").place(x=50,y=380)

        #-----------button------------------------
        btn_register=Button(frame1,text="REGISTER NOW",font=("times new roman",15,'bold'),bg='green',fg="white",cursor="hand2",command=self.register_data)
        btn_register.place(x=50,y=430,width=200,height=40)

        #-----------login button------------------------
        btn_login=Button(self.root,text="Sign In",font=("times new roman",20,'bold'),bg='blue',fg="white",cursor="hand2",command=self.login_window)
        btn_login.place(x=200,y=460,width=180)

    #------------------------------------------------------
    def login_window(self):
        self.root.destroy()
        os.system("python login.py")

    #-------------------------------------------------
    def clear(self):
        self.txt_f_name.delete(0,END)
        self.txt_l_name.delete(0,END)
        self.txt_contact.delete(0,END)
        self.txt_email.delete(0,END)
        self.txt_answer.delete(0,END)
        self.txt_password.delete(0,END)
        self.txt_cnf_password.delete(0,END)
        self.cmb_quest.current(0)
         
    #------------------------------------------------------
    def register_data(self):
        #print(self.var_fname.get(),self.txt_l_name.get())
        if self.txt_f_name.get()=="" or self.txt_contact.get()=="" or self.txt_email.get()=="" or self.cmb_quest.get()=="Select" or self.txt_answer.get()=="" or self.txt_password.get()=="" or self.txt_cnf_password.get()=="":
            messagebox.showerror("Error","All Fields Are Required",parent=self.root)
        elif self.txt_password.get() != self.txt_cnf_password.get():
            messagebox.showerror("Error","Confirm Password Should Be Same",parent=self.root)
        elif self.var_chk.get()==0:
            messagebox.showerror("Error","Please Tick The Box",parent=self.root)
        else:
            try:
                con=sqlite3.connect(database="rms.db")
                cur= con.cursor()
                cur.execute("select * from registration where email=?",(self.txt_email.get(), ))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","User Already Exist",parent=self.root)
                else:
                    cur.execute("insert into registration (fname, lname, contact, email, question, answer, password) values(?,?,?,?,?,?,?)",(
                        self.txt_f_name.get(),
                        self.txt_l_name.get(),
                        self.txt_contact.get(),
                        self.txt_email.get(),
                        self.cmb_quest.get(),
                        self.txt_answer.get(),
                        self.txt_password.get()       
                        ))
                    con.commit()
                    con.close()
                    messagebox.showinfo("Success","Registration Successfully Done",parent=self.root)
                    self.clear()
                    self.login_window()

            except Exception as ex:
                messagebox.showerror("Error",f"Error due to {str(ex)}")

root=Tk()
obj=Register(root)
root.mainloop()