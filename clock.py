from tkinter import*
from PIL import Image,ImageTk,ImageDraw
from datetime import*
import time
from math import*

class clock:
    def __init__(self,root):
        self.root=root
        self.root.title("GUI Analog Clock")
        self.root.geometry("1350x700+0+0")
        self.root.config(bg="#021e2f")
        title=Label(self.root,text="Webcode Analog Clock",font=("times new roman",50,"bold"),bg="#04444a",fg="white").place(x=50,y=50,relwidth=1)
        self.lbl=Label(self.root,bg="white",bd=10,relief=RAISED)
        self.lbl.place(x=450,y=150,width=400,height=400)
        self.working()

    #---------------------------------------------------------
    def clock_img(self,hrs,mins,secs):
        clock=Image.new("RGB",(400,400),(255,255,255))
        draw=ImageDraw.Draw(clock)

        #-----------clock image---------------------
        bg=Image.open("clock.jpg")
        bg=bg.resize((300,300),Image.AFFINE)
        clock.paste(bg,(50,50))

        #---------formula to rotate the needle
        #angle_in_rad=angle_in_deg * math.pi/180
        #line_length=100
        #centre_x=250
        #centre_y=250
        #end_x = centre_x + line_length * math.sin(angle_in_rad)
        #end_y = centre_y - line_length * math.cos(angle_in_rad)

        #-----------hour line image---------------------
        origin=200,200
        draw.line((origin,200+50*sin(radians(hrs)),200-50*cos(radians(hrs))),fill="white",width=4)
        #-----------minute line image---------------------
        draw.line((origin,200+80*sin(radians(mins)),200-80*cos(radians(mins))),fill="blue",width=3)
        #-----------second line image---------------------
        draw.line((origin,200+100*sin(radians(secs)),200-100*cos(radians(secs))),fill="green",width=4)
        #------centre dot---------------
        draw.ellipse((195,195,210,210),fill="white")
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

root=Tk()
obj=clock(root)
root.mainloop()