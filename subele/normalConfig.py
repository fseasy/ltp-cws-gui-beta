#coding=utf-8
import ttk
import os 
import sys
import re
import platform

import Tkinter as tk

class NormalConfig(ttk.Frame) :
    width = 600 
    height = 450
    colnum = 20
    rownum = 10
    cnFont = ("Microsoft YaHei",11)
    def __init__(self , master , basedir) :
        ttk.Frame.__init__(self , master)
        self.basedir = basedir
        self.confdir = os.path.normpath(self.basedir + "/conf")
        if not os.path.exists(self.confdir) :
            os.mkdir(self.confdir)
        self.logdir = os.path.normpath(self.basedir + "/log")
        if not os.path.exists(self.logdir) :
            os.mkdir(self.logdir)
        #make sure the exe path
        self.exePrePath = ''
        self.otExe = "/otcws"
        self.cusOtExe = "/otcws-customized"
        try :
            self.exedir = os.path.normpath(self.basedir + "/ltp-cws-exe")
        
            self.bits = int(re.findall(r'\d+' , platform.architecture()[0])[0])
            #self.system = platform.system()
            sys_str = sys.platform.lower()
            self.system = ""
            if sys_str.startswith("win") :
                self.system = "Windows"
            elif sys_str.startswith("linux") :
                self.system = "Linux"
            elif sys_str.startswith("darwin") :
                self.system = "OSX"
            else :
                self.system = "OTHER"
            #print self.system 
            if self.system == "Linux" and self.bits == 64 :
                self.exePrePath = os.path.normpath(self.exedir + "/linux_amd64/")
            elif self.system == "Linux" and self.bits == 32 :
                self.exePrePath = os.path.normpath(self.exedir + "/linux_i386/")
            elif self.system == "Windows" and self.bits == 64 :
                self.exePrePath = os.path.normpath(self.exedir + '/win_x64/')
                self.otExe += ".exe"
                self.cusOtExe += ".exe"
            elif self.system == "Windows" and self.bits == 32 :
                self.exePrePath = os.path.normpath(self.exedir + '/win_x86/')
                self.otExe += ".exe"
                self.cusOtExe += ".exe"
            elif self.system == "OSX" :
                self.exePrePath = os.path.normpath(self.exedir + '/osx/')
            else :
                self.exePrePath = os.path.normpath(self.exedir + '/other/')
        except Exception , e :
            print e
            self.exePrePath = os.path.normpath(self.exedir + '/other/')
        self.otcwsPath = os.path.normpath(self.exePrePath + self.otExe)
        self.otcwsEnable = os.path.exists(self.otcwsPath)
        self.customOtcwsPath = os.path.normpath(self.exePrePath + self.cusOtExe)
        self.customOtcwsEnable = os.path.exists(self.customOtcwsPath)


    @staticmethod
    def setNormalGrid(target) :
        for i in range(NormalConfig.colnum) :
            target.grid_columnconfigure(i , weight=1 , minsize=NormalConfig.width/NormalConfig.colnum)
        for i in range(NormalConfig.rownum) :
            target.grid_rowconfigure(i , weight=1 , minsize=NormalConfig.height/NormalConfig.rownum)
    @staticmethod
    def setUserGrid(target , row , col , w , h) :
        for i in range(row) :
            target.grid_columnconfigure(i , weight=1 , minsize=h/row)
        for i in range(col) :
            target.grid_rowconfigure(i , weight=1 , minsize=w/col)
    
    @staticmethod
    def setTextTag(target) :
        #text tag
        target.tag_config("head" , foreground="red" , spacing1=10,spacing3=10,justify=tk.CENTER,font=("Microsoft YaHei",14,"bold"),background="#f0f0f0" )
        target.tag_config("text" , foreground="black" ,font=("Courier" , 8))
        target.tag_config("cnText" , foreground="black" ,font=("Microsoft YaHei" , 8))
    
