from tkinter import*
from PIL import Image, ImageTk  #pip install pillow
from tkinter import ttk, messagebox
import sqlite3

class courseClass:
    def __init__(self,root):
        self.root=root
        self.root.title("Student Result Management System")
        self.root.geometry("1200x480+80+170")
        self.root.config(bg="white")
        #self.root.focus_force()           if click nhi krna hover krke krna h toh ye kr


        #-----title----
        title=Label(self.root,text="Manage Course Details",font=("goudy old style",20,"bold"),bg="#033054",fg="white").place(x=10,y=15,width=1180,height=35)


        #------Variable------
        self.var_course=StringVar()
        self.var_duration=StringVar()
        self.var_charges=StringVar()
        self.var_search=StringVar()

        #-----weights-------
        lbl_courseName=Label(self.root,text="Course Name",font=("times new roman",15,"bold"),bg="white").place(x=10,y=60)
        lbl_duration=Label(self.root,text="Duration",font=("times new roman",15,"bold"),bg="white").place(x=10,y=100)
        lbl_charges=Label(self.root,text="Charges",font=("times new roman",15,"bold"),bg="white").place(x=10,y=140)
        lbl_description=Label(self.root,text="Description",font=("times new roman",15,"bold"),bg="white").place(x=10,y=180)

        #------Entries-------
        self.txt_courseName=Entry(self.root,textvariable=self.var_course ,font=("times new roman",15),bg="lightyellow")
        self.txt_courseName.place(x=150,y=60,width=200)
        txt_duration=Entry(self.root,textvariable=self.var_duration,font=("times new roman",15),bg="lightyellow").place(x=150,y=100,width=200)
        txt_charges=Entry(self.root,textvariable=self.var_charges,font=("times new roman",15),bg="lightyellow").place(x=150,y=140,width=200)
        self.txt_description=Text(self.root,font=("times new roman",15),bg="lightyellow")
        self.txt_description.place(x=150,y=180,width=500,height=150)

        #---------buttons----------
        self.btn_add=Button(self.root,text="Save",font=("times new roman",15,'bold'),bg='#2196f3',fg="white",cursor="hand2",command=self.add)
        self.btn_add.place(x=150,y=400,width=110,height=40)
        self.btn_update=Button(self.root,text="Update",font=("times new roman",15,'bold'),bg='#4caf50',fg="white",cursor="hand2",command=self.update)
        self.btn_update.place(x=270,y=400,width=110,height=40)
        self.btn_delete=Button(self.root,text="Delete",font=("times new roman",15,'bold'),bg='#f44336',fg="white",cursor="hand2",command=self.delete)
        self.btn_delete.place(x=390,y=400,width=110,height=40)
        self.btn_clear=Button(self.root,text="Clear",font=("times new roman",15,'bold'),bg='#607d8b',fg="white",cursor="hand2",command=self.clear)
        self.btn_clear.place(x=510,y=400,width=110,height=40)

        #------search panel-----------
        lbl_search_courseName=Label(self.root,text="Course Name",font=("times new roman",15,"bold"),bg="white").place(x=720,y=60)
        txt_search_courseName=Entry(self.root,textvariable=self.var_search ,font=("times new roman",15),bg="lightyellow")
        txt_search_courseName.place(x=870,y=60,width=180)
        btn_search=Button(self.root,text="Search",font=("times new roman",15,'bold'),bg='#03a9f4',fg="white",cursor="hand2",command=self.search)
        btn_search.place(x=1070,y=60,width=120,height=28)

        #--------Content----------
        self.C_Frame=Frame(self.root,bd=2,relief=RIDGE)
        self.C_Frame.place(x=720,y=100,width=470,height=340)

        #----adding scroll bar
        scrolly=Scrollbar(self.C_Frame,orient=VERTICAL)
        scrollx=Scrollbar(self.C_Frame,orient=HORIZONTAL)
        #---------------------------------------------

        self.CoursesTable=ttk.Treeview(self.C_Frame,columns=("Cid","Name","Duration","Charges","Description"),xscrollcommand=scrollx.set,yscrollcommand=scrolly.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)

        scrollx.config(command=self.CoursesTable.xview)
        scrolly.config(command=self.CoursesTable.yview)

        self.CoursesTable.heading("Cid",text="Course ID")
        self.CoursesTable.heading("Name",text="Name")
        self.CoursesTable.heading("Duration",text="Duration")
        self.CoursesTable.heading("Charges",text="Charges")
        self.CoursesTable.heading("Description",text="Description")

        self.CoursesTable["show"]='headings'

        self.CoursesTable.column("Cid",width=100 )
        self.CoursesTable.column("Name",width=100 )
        self.CoursesTable.column("Duration",width=100 )
        self.CoursesTable.column("Charges",width=100)
        self.CoursesTable.column("Description",width=100)
        self.CoursesTable.pack(fill=BOTH,expand=1)

        self.CoursesTable.bind("<ButtonRelease-1>",self.get_data)
        self.show()
############################################################################
    # right table m kisi course pe click krne k baad...data left aa jayega
    def get_data(self, ev):
        self.txt_courseName.config(state='readonly')    #permanenting course name so that user can't change it
        self.txt_courseName

        r=self.CoursesTable.focus()
        content=self.CoursesTable.item(r)
        row=content["values"]
        # print(row)
        self.var_course.set(row[1])
        self.var_duration.set(row[2])
        self.var_charges.set(row[3])
        # self.var_description.set(row[4])
        self.txt_description.delete('1.0',END)
        self.txt_description.insert(END,row[4])

    def add(self):
        con=sqlite3.connect(database="rms.db")
        cur= con.cursor()
        try:
            if self.var_course.get()=="":
                messagebox.showerror("Error","Course Name should be required",parent=self.root)
            else:
                cur.execute("select * from course where name=?",(self.var_course.get(), ))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Course Name already present",parent=self.root)
                else:
                    cur.execute("insert into course (name,duration,charges,description) values(?,?,?,?)",(
                        self.var_course.get(),
                        self.var_duration.get(),
                        self.var_charges.get(),
                        self.txt_description.get("1.0",END)
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Course Added Successfully",parent=self.root)
                    self.show()

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")
###########################################################################################################
    #for update button
    def update(self):
        con=sqlite3.connect(database="rms.db")
        cur= con.cursor()
        try:
            if self.var_course.get()=="":
                messagebox.showerror("Error","Course Name should be required",parent=self.root)
            else:
                cur.execute("select * from course where name=?",(self.var_course.get(), ))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Select Course from list",parent=self.root)
                else:
                    cur.execute("update course set duration=?, charges=?, description=? where name=?",(
                        self.var_duration.get(),
                        self.var_charges.get(),
                        self.txt_description.get("1.0",END),
                        self.var_course.get()
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Course Updated Successfully",parent=self.root)
                    self.show()

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")
###########################################################################################################
    #for clear button
    def clear(self):
        self.show()
        self.var_course.set("")
        self.var_duration.set("")
        self.var_charges.set("")
        self.var_search.set("")
        self.txt_description.delete('1.0',END)
        self.txt_courseName.config(state=NORMAL)

###########################################################################################################
    #for delete button
    def delete(self):
        con=sqlite3.connect(database="rms.db")
        cur= con.cursor()
        try:
            if self.var_course.get()=="":
                messagebox.showerror("Error","Course Name should be required",parent=self.root)
            else:
                cur.execute("select * from course where name=?",(self.var_course.get(), ))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Please Select The Course From The List",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Do you really want to DELETE ?",parent=self.root)
                    if op==True:
                        cur.execute("delete from course where name=?",(self.var_course.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Course Deleted Successfully",parent=self.root)
                        self.clear()

        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")
###########################################################################################################
    #for search button
    def search(self):
        con=sqlite3.connect(database="rms.db")
        cur= con.cursor()
        try:
            cur.execute(f"select * from course where name LIKE '%{self.var_search.get()}%' ")
            rows=cur.fetchall()
            self.CoursesTable.delete(*self.CoursesTable.get_children())
            for row in rows:
                self.CoursesTable.insert('',END,values=row)
                    
        except Exception as ex:
            messagebox.showerror("Error",f"Error due to {str(ex)}")

###########################################################################################
    def show(self):
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



if __name__=="__main__":
    root=Tk()
    obj=courseClass(root)
    root.mainloop()