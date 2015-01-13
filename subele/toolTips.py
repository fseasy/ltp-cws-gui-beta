#coding=utf-8
#http://code.activestate.com/recipes/576688-tooltip-for-tkinter/
# withdraw : hide the window , using deiconify() restore it 
# after (milliseconds , callback )  
from Tkinter import *
from time import time , localtime , strftime

class ToolTip(Toplevel) :
    def __init__(self , wdgt , msg=None , msgFunc=None , delay=1 ,follow=True) :
        self.wdgt = wdgt
        self.parent = self.wdgt.master
        Toplevel.__init__(self , self.parent , bg='black' , padx=1 , pady=1)
        self.withdraw()
        self.overrideredirect( True )
        
        self.msgVar = StringVar()
        if msg == None :
            self.msgVar.set("")
        else :
            self.msgVar.set( msg )
        self.msgFunc = msgFunc 
        self.delay = delay
        self.follow = follow
        self.visible = 0
        self.lastMotion = 0
        
        Message(self , textvariable=self.msgVar , bg="#FFFFDD" , aspect=1000).grid()
        self.wdgt.bind('<Enter>' , self.spawn , '+')
        self.wdgt.bind('<Leave>' , self.hide , '+')
        self.wdgt.bind('<Motion>' , self.move , '+')
        
    def spawn(self , event=None) :
        self.visible = 1 
        self.after(int(self.delay * 1000) , self.show)
        
    def show(self) :
        if self.visible == 1 and time() - self.lastMotion > self.delay : 
            self.visible = 2 
        if self.visible == 2 :
            self.deiconify()
    
    def move(self , event) :
        self.lastMotion = time()
        if self.follow == False :
            self.withdraw()
            self.visible = 1
        self.geometry("+%i+%i" %( event.x_root , event.y_root + 10))
        try :
            self.msgVar.set(self.msgFunc())
        except :
            pass
        self.after(int(self.delay* 1000) , self.show)
    
    def hide(self , event=None) :
        self.visible = 0 
        self.withdraw()
