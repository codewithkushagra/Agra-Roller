import tkinter
from tkinter import *
import Data_Base
from tkinter.ttk import *
from PIL import ImageTk, Image 
import time
from tkinter.constants import *
from tkinter import messagebox
import os

tk = tkinter.Tk()
tk.title("Agar Roller GPS Tracker")
tk.geometry('%dx%d+0+0'%(tk.winfo_screenwidth(),tk.winfo_screenheight()))
tk.resizable(height=None, width=None)




img = ImageTk.PhotoImage(Image.open("map_final.png"))  
frame_GSP = tkinter.Label(tk, image = img) 
frame_GSP.grid(row=1,column=0,sticky="news")




frame_button = tkinter.Frame(tk, borderwidth=2,bg="blue")
frame_button.grid(row=0,column=0)
#frame_GSP = tkinter.Frame(tk, borderwidth=2)
#frame_GSP.grid(row=1,column=0,sticky="news")
frame_Allot = tkinter.Frame(tk, borderwidth=2)
frame_Allot.grid(row=1,column=0,sticky="news",ipady=300,ipadx=500)

run=StringVar()

allote=tkinter.Button(frame_button,text="Allot IMEI Number",width=30,height=5,command=lambda :show(frame_Allot,False) ,font="Times 10")
allote.grid(row=0,column=0,padx=275)

gps=tkinter.Button(frame_button,text="GPS",width=30,height=5,command=lambda :show(frame_GSP,True),font="Times 10")
gps.grid(row=0,column=1,padx=275)

def show(frame,runt):  
    frame.tkraise()
    if runt:
        run.set("1")
        gpstack()
    else:
        run.set("0")
    return
    return
imei=StringVar()

def gpstack():
    if run.get()=="1":
        refresh=tkinter.Button(frame_GSP,text="Refresh",command=lambda :show(frame_GSP,True),font="Times 10")
        refresh.pack()
        refresh.place(x=0,y=0)
        gps_data=Data_Base.getLastdata_location_data()
        for i in gps_data:
            yc=i[2]
            xc=i[3]
        print(yc)
        print(xc)
        print("")
        #qbit1=tkinter.Label(frame_GSP,text="A")
        #qbit1.pack()
        #qbit1.place(x=950,y=590)
        #qbit2=tkinter.Label(frame_GSP,text="D")
        #qbit2.pack()
        #qbit2.place(x=560,y=590)
        #qbit3=tkinter.Label(frame_GSP,text="C")
        #qbit3.pack()
        #qbit3.place(x=560,y=5)
        #qbit4=tkinter.Label(frame_GSP,text="B")
        #qbit4.pack()
        #qbit4.place(x=950,y=5)
        #27.219926039489113, 77.92110778739176
        #xc=140257994
            #27.219201117424834, 77.92118799616959
        #yc=48995866
        xc=xc-140257218
        yc=48997375-yc
        xc=xc*(390/(140260273-140257218))
        yc=yc*(585/(48997375-48993336))
        xc=xc+560
        yc=yc+5
        qbit1=tkinter.Label(frame_GSP,text="0")
        qbit1.pack()
        qbit1.place(x=xc,y=yc)
        # qbit1.destroy()
        
    return

def allotlist():
    
    def data():
        btn=[]
        allot=["None"]
        p=0
        ccc=0 
        all_data=Data_Base.getAlldata_allot()
        allot_data=Data_Base.getIMEI()        
        for i in allot_data:
            allot.append(i[0])
        o=1
        def update(c):
            Data_Base.update(c,imei.get())
            allotlist()
            return
        def f(c,h,pp):
            k=tkinter.OptionMenu(frame,imei,*allot)
            imei.set(allot[0])
            k.grid(row=pp+1,column=30)
            Button(frame, text="Done", command=lambda :update(c)).grid(row=pp+1,column=40)
            return
        Label(frame,text="           Sno.           ",font="Time 14").grid(row=0,column=0)
        Label(frame,text="   Employee Name  ",font="Time 14").grid(row=0,column=5)
        Label(frame,text="          IMEI     ",font="Time 14").grid(row=0,column=10)
        for i in all_data:
            Label(frame,text=i[0],font="Time 12").grid(row=o,column=0)
            Label(frame,text=i[1],font="Time 12").grid(row=o,column=5)
            Label(frame,text=i[2],font="Times 12").grid(row=o,column=10)
            btn.append(Button(frame, text="Change", command=lambda h=p,c=i[1],pp=ccc:f(c,h,pp)))
            btn[p].grid(row=o,column=15)
            p+=1
            o+=1
            ccc+=1            
        return      
    def myfunction(event):
        canvas.configure(scrollregion=canvas.bbox("all"),width=1200,height=540)
    
    myframe=tkinter.Frame(frame_Allot,relief=GROOVE,width=1000,height=1000,bd=1)
    myframe.place(x=10,y=130)
    canvas=tkinter.Canvas(myframe)
    frame=tkinter.Frame(canvas)
    myscrollbar=tkinter.Scrollbar(myframe,orient="vertical",command=canvas.yview)
    myscrollbar1=tkinter.Scrollbar(myframe,orient="horizontal",command=canvas.xview)
    canvas.configure(yscrollcommand=myscrollbar.set)
    canvas.configure(xscrollcommand=myscrollbar1.set)
    myscrollbar1.pack(side="bottom",fill="x")
    myscrollbar.pack(side="right",fill="y")
    canvas.pack(side="left")
    canvas.create_window((0,0),window=frame,anchor='nw')
    frame.bind("<Configure>",myfunction)
    data()

    return


allotlist()
tk.mainloop()
