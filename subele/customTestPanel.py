#coding=utf-8

import Tkinter as tk
import ttk
import tkFileDialog
import tkFont

import sys
import os
import subprocess
import threading
import time

from normalConfig import NormalConfig
from normalEventHandler import NormalEventHandler
from generalFunction import *
from toolTips import ToolTip

class CustomTestPanel(ttk.Frame) :
    def __init__(self ,  master , conf) :
        ttk.Frame.__init__(self , master)
        NormalConfig.setNormalGrid(self)
        self.conf = conf ;
        self.confPath = os.path.normpath(self.conf.confdir + "/customTest.conf")
        
        self.saveDataPath = ""
        self.logPath = os.path.normpath(self.conf.logdir + "/customTest.log")

        self.outFile = None
        self.logFile = None 
        self.isWordThreadEnd = True
        
        self.createWidgets()
        self.updateEntry()
        
    def createWidgets(self) :
    
        ttk.Label(self , text="测试集文件路径" , font=NormalConfig.cnFont).grid(row=0,column=0 , columnspan=6 , padx=10 , sticky=tk.W + tk.E)
        self.testDataEntry = ttk.Entry(self)
        self.testDataEntry.grid(row=0 , column=6 , columnspan=10 , sticky=tk.W+tk.E)
        self.testDataBtn = ttk.Button(self , text="浏览" , command=lambda : NormalEventHandler.openFileDialogAndSetEntryValue(self.testDataEntry))
        self.testDataBtn.grid(row=0 , column=17 , columnspan=2)

        ttk.Label(self , text="基础模型文件路径" , font=NormalConfig.cnFont).grid(row=1,column=0 , columnspan=6 , padx=10 , sticky=tk.W + tk.E)
        self.basicModelEntry = ttk.Entry(self)
        self.basicModelEntry.grid(row=1 , column=6 , columnspan=10 , sticky=tk.W+tk.E)
        self.basicModelBtn = ttk.Button(self , text="浏览" , command=lambda : NormalEventHandler.openFileDialogAndSetEntryValue(self.basicModelEntry))
        self.basicModelBtn.grid(row=1 , column=17 , columnspan=2)
        
        ttk.Label(self , text="个性化模型文件路径" , font=NormalConfig.cnFont).grid(row=2,column=0 , columnspan=6 , padx=10 , sticky=tk.W + tk.E)
        self.customModelEntry = ttk.Entry(self)
        self.customModelEntry.grid(row=2 , column=6 , columnspan=10 , sticky=tk.W+tk.E)
        self.customModelBtn = ttk.Button(self , text="浏览" , command=lambda : NormalEventHandler.openFileDialogAndSetEntryValue(self.customModelEntry))
        self.customModelBtn.grid(row=2 , column=17 , columnspan=2)

        ttk.Label(self , text="测试结果保存路径" , font=NormalConfig.cnFont).grid(row=3,column=0 , columnspan=6 , padx=10 , sticky=tk.W + tk.E)
        self.saveDataEntry = ttk.Entry(self)
        self.saveDataEntry.grid(row=3 , column=6 , columnspan=10 , sticky=tk.W+tk.E)
        self.saveDataBtn = ttk.Button(self , text="浏览" , command=lambda : NormalEventHandler.saveasFileDialogAndSetEntryValue(self.saveDataEntry))
        self.saveDataBtn.grid(row=3 , column=17 , columnspan=2)

        self.testBtn = ttk.Button(self , text="个性化模型训练" )
        self.testBtn.grid(row=4 , column=0 , columnspan=6 , padx=10 , sticky=tk.W)
        
        #ouput
        self.outFrame = ttk.LabelFrame(self , text="部分输出结果")
        self.outFrame.grid(row=5 , column=0 , rowspan=2 , columnspan=20 , sticky=tk.W+tk.E+tk.N + tk.S)
        NormalConfig.setUserGrid(self.outFrame , 1 , 30 , self.outFrame.winfo_reqwidth() , self.outFrame.winfo_reqheight())
        self.outText = createTextWithScroll(self.outFrame) 

        #log
        self.logFrame = ttk.LabelFrame(self , text="日志输出")
        self.logFrame.grid(row=7 , column=0 , rowspan=2 , columnspan=20 , sticky=tk.W+tk.E+tk.N+tk.S)
        NormalConfig.setUserGrid(self.logFrame , 1 , 30 , self.logFrame.winfo_reqwidth() , self.logFrame.winfo_reqheight())
        self.logText = createTextWithScroll(self.logFrame)

    def updateEntry(self) :
        if os.path.exists(self.confPath) :
            try :
                confFile = open(self.confPath , 'r')
                conts = confFile.readlines()
                self.testDataEntry.insert(0,conts[1].split(" = ")[1].strip(" \n\r"))
                self.basicModelEntry.insert(0,conts[3].split(" = ")[1].strip(" \r\n"))
                self.customModelEntry.insert(0,conts[2].split(" = ")[1].strip(" \r\n"))
                confFile.close()
            except :
                pass
                
    def isRunable(self) :
        #check 
        testDataPath = os.path.normpath(self.testDataEntry.get())
        basicModelPath = os.path.normpath(self.basicModelEntry.get())
        customModelPath = os.path.normpath(self.customModelEntry.get())
        
        self.saveDataPath = os.path.normpath(self.saveDataEntry.get())
        
        #print "1:%s\n2:%s\n3:%s" %(testDataPath , modelDataPath , self.saveDataPath)
        
        if(not os.path.exists(testDataPath) or not os.path.exists(basicModelPath) or not os.path.exists(customModelPath)) :
            tkMessageBox.showerror("错误" , "请选择正确的测试集文件路径和各模型路径")
            return False
        
        saveDataDir = os.path.dirname(self.saveDataPath)
        if not os.path.exists(saveDataDir) :
            tkMessageBox.showerror("错误" , "请选择正确的结果输出路径")
            return False
        #mk conf
        #baseline-model-file = basic.4.model
        #customized-model-file = model/ctb5-seg.4.model
        confContent = '\n'.join([
            '[test]' ,
            'test-file = ' + testDataPath ,
            'customized-model-file = ' + customModelPath ,
            'baseline-model-file = ' + basicModelPath ,
            ])
        try :
            confFile = open(self.confPath , 'w')
            confFile.write(confContent)
            confFile.close()
        except IOError :
            tkMessageBox.showerror("错误" , "内部配置文件写入错误")
            print >>sys.stderr , confContent
            return False
        if self.conf.otcwsEnable :
            self.cmdstr = ' '.join([self.conf.otcwsPath , self.confPath , '>' , self.saveDataPath , '2>' , self.logPath])
            #print self.cmdstr
            return True
        else :
            tkMessageBox.showerror("错误" , "未找到适合该平台的分词程序\nsystem info : %s , %s bits" %(self.conf.system , self.conf.bits))
            print self.conf.otcwsPath
            return False
    
    def updateLog(self) :
        self.logText.insert(tk.END , "开始个性化模型测试\n" , "head")
        try :
            self.logFile = open(self.logPath)
            self.outFile = open(self.saveDataPath)
        except :
            print >>sys.stderr , "outFile / logFile open error"
            print >>sys.stderr , self.logPath
            print >>sys.stderr , self.saveDataPath
            return 
        while not self.isWorkThreadEnd :
            outCont = tail(self.outFile,2)
            if outCont != '' :
                self.outText.insert(tk.END , outCont , "cnText")
                self.outText.yview(tk.MOVETO , 1 )
            logCont = self.logFile.read()
            if logCont != "" :
                self.logText.insert(tk.END , logCont , "text")
                self.logText.see(tk.END)
            time.sleep(1.5)
        try :
            self.outFile.close()
            self.logFile.close()
        except :
            pass
        #self.logText.config(state=tk.NORMAL) 
        self.logText.insert(tk.END , "模型测试完成.\n" , "head")
        self.logText.insert(tk.END ,"日志文件地址:"+ self.logPath +"\n" , "text")
        try :
            self.logText.yview(tk.MOVETO , 1)
            self.logText.config(state=tk.DISABLED)
            self.outText.config(state=tk.DISABLED)
        except :
            pass
        try :
            subprocess.Popen("explorer /select,"+self.saveDataPath)
        except Exception , e :
            print e
        
    def work(self) :
        self.workThread = threading.Thread(target=self.cmdWork , args=(self.cmdstr ,))
        
        self.isWorkThreadEnd = False
        #ui init should at main thread
        self.logText.config(state=tk.NORMAL)
        self.outText.config(state=tk.NORMAL)
        #start threads
        self.workThread.start()
        threading.Thread(target=self.updateLog).start()
        
        
        
    def cmdWork(self , cmdStr) :
        self.isWordThreadEnd = False 
        subp = subprocess.Popen(cmdStr , shell=True) 
        subp.wait()
        self.isWorkThreadEnd = True
