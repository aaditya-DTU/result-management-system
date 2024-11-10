from tkinter import*
from PIL import Image,ImageTk,ImageDraw
from datetime import*
import time
from math import*
import sqlite3
from tkinter import ttk,messagebox
import os

class login_window:
    def __init__(self,root):
        self.root=root
        self.root.title("Login Portal")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="#021e2f")
        
        #-----------background color------------
        left_lbl=Label(self.root,bg="#08A3D2",bd=0)
        left_lbl.place(x=0,y=0,width=600,relheight=1)
        
        right_lbl=Label(self.root,bg="#031F3C",bd=0)
        right_lbl.place(x=600,y=0,relwidth=1,relheight=1)

        #---------------frames------------------
        login_frame=Frame(self.root,bg="white")
        login_frame.place(x=250,y=100,width=800,height=500)
        #---title---------
        title=Label(login_frame,text="LOGIN HERE",font=("times new roman",30,"bold"),bg="white",fg="#08A3D2").place(x=250,y=50)
        #---email-------
        email=Label(login_frame,text="EMAIL ADDRESS",font=("times new roman",18,"bold"),bg="white",fg="black").place(x=250,y=150)
        self.txt_email=Entry(login_frame,font=("times new roman",15),bg="lightblue")
        self.txt_email.place(x=250,y=180,width=350,height=35)
        #---email password-------
        email_pass=Label(login_frame,text="PASSWORD",font=("times new roman",18,"bold"),bg="white",fg="black").place(x=250,y=250)
        self.txt_email_pass=Entry(login_frame,font=("times new roman",15),bg="lightblue")
        self.txt_email_pass.place(x=250,y=280,width=350,height=35)
        #------registration button------------
        btn_reg=Button(login_frame,text="Register Now",font=("times new roman",14),bg="white",bd=0,fg="#B00857",cursor="hand2",command=self.reg_window).place(x=250,y=320)
        #------forget button------------
        btn_forget=Button(login_frame,text="Forget Password ?",font=("times new roman",14),bg="white",bd=0,fg="red",cursor="hand2",command=self.forget_window).place(x=450,y=320)
        #-----login button--------------
        btn_login=Button(login_frame,text="Login",font=("times new roman",20,"bold"),fg="white",bg="#B00857",cursor="hand2",command=self.login).place(x=250,y=380,width=180,height=40)


        #-------------clock----------------
        self.lbl=Label(self.root,text="\nWebcode Clock",font=("Book Antiqua",25,"bold"),fg="white",compound=BOTTOM,bg="orange",bd=0)
        self.lbl.place(x=90,y=120,width=350,height=450)
        self.working()

    #---------------------------------------------------------
    def clock_img(self,hrs,mins,secs):
        clock=Image.new("RGB",(400,400),(0,0,0))
        draw=ImageDraw.Draw(clock)

        #-----------clock image---------------------
        bg=Image.open("clock.jpg")
        bg=bg.resize((300,300),Image.AFFINE)
        clock.paste(bg,(50,50))

        #-----------hour line image---------------------
        origin=200,200
        draw.line((origin,200+50*sin(radians(hrs)),200-50*cos(radians(hrs))),fill="white",width=4)
        #-----------minute line image---------------------
        draw.line((origin,200+80*sin(radians(mins)),200-80*cos(radians(mins))),fill="blue",width=3)
        #-----------second line image---------------------
        draw.line((origin,200+100*sin(radians(secs)),200-100*cos(radians(secs))),fill="green",width=2)
        #------centre dot---------------
        draw.ellipse((195,195,210,210),fill="#1AD5D5")
        clock.save("clock_new.png")

    #-----------------------------------------------------
    def working(self):
        h=datetime.now().time().hour
        m=datetime.now().time().minute
        s=datetime.now().time().second
        #-------changing into angles-------------------
        hr_=(h/12)*360
        min_=(m/60)*360
        sec_=(s/60)*360

        self.clock_img(hr_,min_,sec_)
        self.img=ImageTk.PhotoImage(file="clock_new.png")
        self.lbl.config(image=self.img)
        self.lbl.after(200,self.working)

    #----------------------------------------------
    def reset(self):
        self.cmb_quest.current(0)
        self.txt_new_pass.delete(0,END)
        self.txt_answer.delete(0,END)
        self.txt_email_pass.delete(0,END)
        self.txt_email.delete(0,END)

    #----------------------------------------------
    def forget_pass(self):
        if self.cmb_quest.get=="Select" or self.txt_answer.get()=="" or self.txt_new_pass.get()=="":
            messagebox.showerror("Error","All Fields Are Required",parent=self.root2)
        else:
            try:
                con=sqlite3.connect("rms.db")
                cur=con.cursor()
                cur.execute("select * from registration where email=? and question=? and answer=? ",(self.txt_email.get(),self.cmb_quest.get(),self.txt_answer.get()))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Please Select Correct Question / Answer",parent=self.root2)
                else:
                    cur.execute("update registration set password=? where email=?",(self.txt_new_pass.get(),self.txt_email.get()))
                    con.commit()
                    con.close()
                    messagebox.showinfo("Success","Password Updated Successfully !",parent=self.root2)
                    self.reset()
                    self.root2.destroy()
            except Exception as es:
                messagebox.showerror("Error",f"Error Due To: {str(es)}",parent=self.root)

    #----------------------------------------------
    def forget_window(self):
        if self.txt_email.get()=="":
            messagebox.showerror("Error","Please Enter Email Address To Reset Your Password",parent=self.root)
        else:
            try:
                con=sqlite3.connect("rms.db")
                cur=con.cursor()
                cur.execute("select * from registration where email=? ",(self.txt_email.get(), ))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Please Enter A Valid Email Address To Reset Your Password",parent=self.root)
                else:
                    #self.root2=Tk()
                    con.close()
                    self.root2=Toplevel()
                    self.root2.title("Forget Password")
                    self.root2.geometry("350x400+495+150")
                    self.root2.config(bg="white")
                    self.root2.focus_force()
                    self.root2.grab_set()

                    t=Label(self.root2,text="Forget Password",font=("times new roman",20,"bold"),bg="white",fg="red").place(x=0,y=10,relwidth=1)

                    question=Label(self.root2,text="Security Question",font=("times new roman",15,"bold"),bg="white",fg="black").place(x=50,y=80)
                    self.cmb_quest=ttk.Combobox(self.root2,font=("times new roman",13),state='readonly',justify=CENTER)
                    self.cmb_quest['values']=("Select","Your First Pet Name","Your Birth Place","Your Best Friend Name")
                    self.cmb_quest.place(x=50,y=110,width=250)
                    self.cmb_quest.current(0)

                    answer=Label(self.root2,text="Answer",font=("times new roman",15,"bold"),bg="white",fg="black").place(x=50,y=160)
                    self.txt_answer=Entry(self.root2,font=("times new roman",15),bg="lightyellow")
                    self.txt_answer.place(x=50,y=190,width=250)

                    new_pass=Label(self.root2,text="New Password",font=("times new roman",15,"bold"),bg="white",fg="black").place(x=50,y=240)
                    self.txt_new_pass=Entry(self.root2,font=("times new roman",15),bg="lightyellow")
                    self.txt_new_pass.place(x=50,y=270,width=250)

                    btn_change_pass=Button(self.root2,text="Reset Password",font=("times new roman",15,"bold"),fg="white",bg="green",cursor="hand2",command=self.forget_pass).place(x=90,y=330)
                
            except Exception as es:
                    messagebox.showerror("Error",f"Error Due To: {str(es)}",parent=self.root)   

    #----------------------------------------------
    def reg_window(self):
        self.root.destroy()
        import register

    #-----------------------------------------------
    def login(self):
        if self.txt_email.get()=="" or self.txt_email_pass.get()=="":
            messagebox.showerror("Error","All Fields Are Required",parent=self.root)
        else:
            try:
                con=sqlite3.connect("rms.db")
                cur=con.cursor()
                cur.execute("select * from registration where email=? and password=?",(self.txt_email.get(),self.txt_email_pass.get()))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Invalid Username & Password",parent=self.root)
                else:
                    messagebox.showinfo("Success",f"Welcome Back {self.txt_email.get()})",parent=self.root)
                    self.root.destroy()
                    os.system("python studentDashboard.py")
                con.close()
            except Exception as es:
                messagebox.showerror("Error",f"Error Due To: {str(es)}",parent=self.root)


root=Tk()
obj=login_window(root)
root.mainloop()