from tkinter import*
from PIL import Image, ImageTk, ImageDraw  #pip install pillow
from courses import courseClass
from student import studentClass
from result import resultClass
from report_card import reportClass
from tkinter import messagebox
import os
from datetime import*
import time
from math import*
import sqlite3

class RMS:
    def __init__(self,root):
        self.root=root
        self.root.title("Student Result Management System")
        self.root.geometry("1350x7000+0+0")
        self.root.config(bg="white")

        #------icons---
        #self.logo_dash=ImageTk.PhotoImage(file="pngwing.com.png")  padx=10,compound=LEFT,image=self.logo_dash
        #-----title----
        title=Label(self.root,text="Student Result Management System",font=("goudy old style",20,"bold"),bg="#033054",fg="white").place(x=0,y=0,relwidth=1,height=50)
        #-----MEnu-----
        M_Frame=LabelFrame(self.root,text="Menu",font=("times new roman",15),bg="white")
        M_Frame.place(x=10,y=70,width=1340,height=80)

        btn_course=Button(M_Frame,text="Course",font=("goudy old style",15,"bold"),bg="#00BFFF",fg="white",cursor="hand2",command=self.add_course).place(x=20,y=5,width=200,height=40)
        btn_student=Button(M_Frame,text="Student",font=("goudy old style",15,"bold"),bg="#00BFFF",fg="white",cursor="hand2",command=self.add_student).place(x=240,y=5,width=200,height=40)
        btn_result=Button(M_Frame,text="Result",font=("goudy old style",15,"bold"),bg="#00BFFF",fg="white",cursor="hand2",command=self.add_result).place(x=460,y=5,width=200,height=40)
        btn_view=Button(M_Frame,text="View Student Result",font=("goudy old style",15,"bold"),bg="#00BFFF",fg="white",cursor="hand2",command=self.add_report).place(x=680,y=5,width=200,height=40)
        btn_logout=Button(M_Frame,text="Logout",font=("goudy old style",15,"bold"),bg="#00BFFF",fg="white",cursor="hand2",command=self.add_logout).place(x=900,y=5,width=200,height=40)
        btn_exit=Button(M_Frame,text="Exit",font=("goudy old style",15,"bold"),bg="#00BFFF",fg="white",cursor="hand2",command=self.add_exit).place(x=1120,y=5,width=200,height=40)
        #0b5377

        #-----content----
        self.bg_img=Image.open("result_pic.png")
        self.bg_img=self.bg_img.resize((920,350),Image.AFFINE)
        self.bg_img=ImageTk.PhotoImage(self.bg_img)

        self.lbl_bg=Label(self.root,image=self.bg_img).place(x=400,y=180,width=920,height=350)

        #------update_details-----
        self.lbl_course=Label(self.root,text="Total Courses\n[ 0 ]",font=("goudy old style",20),bd=10,relief=RIDGE,bg="#e43b06",fg="white")
        self.lbl_course.place(x=400,y=530,width=300,height=100)

        self.lbl_student=Label(self.root,text="Total Students\n[ 0 ]",font=("goudy old style",20),bd=10,relief=RIDGE,bg="#0676ad",fg="white")
        self.lbl_student.place(x=710,y=530,width=300,height=100)

        self.lbl_result=Label(self.root,text="Total Results\n[ 0 ]",font=("goudy old style",20),bd=10,relief=RIDGE,bg="#038074",fg="white")
        self.lbl_result.place(x=1020,y=530,width=300,height=100)
        
        #-------------clock----------------
        self.lbl=Label(self.root,text="\nWebcode Clock",font=("Book Antiqua",25,"bold"),fg="white",compound=BOTTOM,bg="orange",bd=0)
        self.lbl.place(x=10,y=180,width=350,height=450)
        self.working()
        
        #-----footer----
        footer=Label(self.root,text="SRMS-Student Result Management System\nContact Us For Any Technical Issue: 9643795074",font=("goudy old style",12),bg="#262626",fg="white").pack(side=BOTTOM,fill=X)

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

    #---------------------------------------
    def update_details(self):
        con=sqlite3.connect(database="rms.db")
        cur= con.cursor()
        try:
            cur.execute("select * from course")
            rows=cur.fetchall()

            #debuging test
            print(rows)

            self.CoursesTable.delete(*self.CoursesTable.get_children())
            for row in rows:
                self.CoursesTable.insert('',END,values=row)
                    
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")


    #----------working--------------
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

    #-------linking courses details-------
    def add_course(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=courseClass(self.new_win)

    #-------linking student details-------
    def add_student(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=studentClass(self.new_win)

    #-------linking result details-------
    def add_result(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=resultClass(self.new_win)

    #-------linking report card details-------
    def add_report(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=reportClass(self.new_win)

    #-------linking login page-------
    def add_logout(self):
        op=messagebox.askyesno("Confirm","Do you really want to logout?",parent=self.root)
        if op==TRUE:
            self.root.destroy()
            os.system("python login.py")

    #-------linking login page-------
    def add_exit(self):
        op=messagebox.askyesno("Confirm","Do you really want to exit?",parent=self.root)
        if op==TRUE:
            self.root.destroy()


if __name__=="__main__":
    root=Tk()
    obj=RMS(root)
    root.mainloop()