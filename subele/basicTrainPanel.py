#coding=utf-8
import Tkinter as tk
import ttk
import tkFileDialog
import tkFont
import tkMessageBox

import os
import sys
import subprocess
import threading
import time

from normalConfig import NormalConfig
from normalEventHandler import NormalEventHandler
from generalFunction import * 

class BasicTrainPanel(ttk.Frame) :
    def __init__(self , master , conf) :
        ttk.Frame.__init__(self , master )
        self.grid_propagate(False)
        #for i in range(10) :
        #    self.grid_columnconfigure(i , weight=1 , minsize=30)
        NormalConfig.setNormalGrid(self);
        self.conf = conf 
        
        self.confPath = os.path.normpath(self.conf.confdir + "/basicTrain.conf")
        self.saveDataPath = ""
        self.logPath = os.path.normpath(self.conf.logdir + "/basicTrain.log")
        
        self.logFile = None
        self.isWorkThreadEnd = True
        
        self.createWidgets()
        self.updateEntry()
        
    def createWidgets(self) :
        self.trainingDataLabel = ttk.Label(self , text="训练集文件路径", font=NormalConfig.cnFont )
        self.trainingDataLabel.grid(row=0 , column=0 , columnspan=6,sticky=tk.W+tk.E , padx=10 )
        self.trainingDataEntry = ttk.Entry(self)
        self.trainingDataEntry.grid(row=0 , column=6 , columnspan=10 , sticky=tk.W + tk.E) #padding 1 col
        self.trainingDataBtn = ttk.Button(self , text="浏览" , command=lambda : NormalEventHandler.openFileDialogAndSetEntryValue(self.trainingDataEntry))
        self.trainingDataBtn.grid(row=0 , column=17 , columnspan=2)
        
        self.devDataLabel = ttk.Label(self , text="开发集文件路径" , font=NormalConfig.cnFont) 
        self.devDataLabel.grid(row=1 , column=0 , columnspan=6, padx=10 , sticky=tk.W+tk.E)
        self.devDataEntry = ttk.Entry(self)
        self.devDataEntry.grid(row=1 , column=6 , columnspan=10 , sticky=tk.E+tk.W)
        self.devDataBtn = ttk.Button(self , text="浏览" , command=lambda : NormalEventHandler.openFileDialogAndSetEntryValue(self.devDataEntry))
        self.devDataBtn.grid(row=1 , column=17 , columnspan=2)

        self.saveDataLabel = ttk.Label(self , text="基础模型保存路径" , font=NormalConfig.cnFont)
        self.saveDataLabel.grid(row=2 , column=0 , columnspan=6, padx=10 , sticky=tk.W+tk.E)
        self.saveDataEntry = ttk.Entry(self)
        self.saveDataEntry.grid(row=2 , column=6 , columnspan=10 , sticky=tk.E+tk.W)
        self.saveDataBtn = ttk.Button(self , text="浏览" , command=lambda : NormalEventHandler.saveasFileDialogAndSetEntryValue(self.saveDataEntry))
        self.saveDataBtn.grid(row=2 , column=17 , columnspan=2 )
        
        self.maxIteLabel = ttk.Label(self , text="训练最大迭代次数" , font=NormalConfig.cnFont).grid(row=3,column=0 , columnspan=6 , padx=10 , sticky=tk.W + tk.E )
        self.maxIteEntry = ttk.Entry(self, width=2)
        self.maxIteEntry.grid(row=3 , column=6 , sticky=tk.W + tk.E)
        self.maxIteEntry.insert(0,"5")
   
        self.trainBtn = ttk.Button(self , text="基础模型训练" , command=lambda : NormalEventHandler.workAction(self))
        self.trainBtn.grid(row=4 , column=0 , columnspan=5 , padx=10 , sticky=tk.W)
        
        self.trainTipsVar = tk.StringVar()
        self.trainTips= ttk.Label(self , textvariable=self.trainTipsVar , font=("Microsoft YaHei" , 8) , foreground="red")
        self.trainTipsVar.set("点击按钮开始训练")
        self.trainTips.grid(row=4 , column=5 , columnspan=13 , sticky=tk.W)
        
        self.logFrame = ttk.Labelframe(self , text="训练日志输出")
        self.logFrame.grid(row=6 , column=0 , rowspan=3 , columnspan=20 , sticky=tk.W+tk.N+tk.S+tk.E)
        NormalConfig.setUserGrid(self.logFrame , 1 , 30 , self.logFrame.winfo_reqwidth() , self.logFrame.winfo_reqheight())
        self.logText = createTextWithScroll(self.logFrame) ;
    
    def updateEntry(self) :
        if os.path.exists(self.confPath) :
            try :
                confFile = open(self.confPath , 'r')
                conts = confFile.readlines()
                self.trainingDataEntry.insert(0,conts[1].split(" = ")[1].strip(" \n\r"))
                self.devDataEntry.insert(0,conts[2].split(" = ")[1].strip(" \r\n"))
                self.saveDataEntry.insert(0,conts[4].split(" = ")[1].strip(" \r\n"))
                confFile.close()
            except :
                pass    
                
    def isRunable(self) :
        #--check--
        #check path and iterator number
        trainDataPath = os.path.normpath(self.trainingDataEntry.get())
        devDataPath = os.path.normpath(self.devDataEntry.get())
        self.saveDataPath = os.path.normpath(self.saveDataEntry.get())
        self.maxIte = self.maxIteEntry.get()
        
        if not os.path.exists(trainDataPath) or not os.path.exists(devDataPath) :
            tkMessageBox.showerror("错误" , "请选择正确的训练集文件路径和开发集路径")
            return False
        modelDir = os.path.dirname(self.saveDataPath)
        if not os.path.exists(modelDir) :
            tkMessageBox.showerror("错误","请选择正确的模型输出路径")
            return False
        try :
            self.maxIte = int(self.maxIte)
            if self.maxIte < 1 :
                raise Exception
        except :
            tkMessageBox.showerror("错误", "请输入合法的最大迭代次数")
            return False
        #write the conf to the file
        confCont = "\n".join([
            "[train]" ,
            "train-file = " + trainDataPath ,
            "holdout-file = " + devDataPath ,
            "algorithm = pa" ,
            "model-name = " + self.saveDataPath ,
            "max-iter = " + str(self.maxIte) ,
            "enable-incremental-training = 1" ,
            "rare-feature-threshold = 0"
        ])
        try :
            confFile = open(self.confPath , "w")
            confFile.write(confCont)
            confFile.close()
        except :
            tkMessageBox.showerror("错误" , "内部配置文件写入错误")
            print >>sys.stderr , confCont
            return False
        #check exe
        if self.conf.otcwsEnable :
            self.cmdstr = ' '.join([
                self.conf.otcwsPath ,
                self.confPath ,
                # "> " + self.saveDataPath ,
                "2> " + self.logPath 
            ])
            print self.cmdstr
            return True
        else :
            tkMessageBox.showerror("错误" , "未找到适合该平台的分词程序\nsystem info : %s , %s bits" %(self.conf.system , self.conf.bits))
            print self.conf.otcwsPath
            return False
    
    def updateLog(self) :
        
        self.logText.insert(tk.END , "开始训练\n" ,"head")
        self.logText.update()
        #open log file
        try_times = 3
        while try_times > 0 :
            try :
                self.logFile = open(self.logPath) # if this thread run before the workThread , it may cause error : the file has not been create
                if try_times != 3 :
                    self.trainTipsVar.set("训练时间较长,请耐心等待,不要关掉程序.")
                break
            except :
                self.testTipsVar.set("读取LOG文件失败.剩余重试次数:"+str(try_times-1))
                time.sleep(4)
                try_times -= 1
        else :
            self.logFile = None
        while not self.isWorkThreadEnd and self.logFile != None :
            cont = self.logFile.read()
            if cont != '' :
                self.logText.insert(tk.END , cont , "text")
                self.logText.yview(tk.MOVETO , 1)
            time.sleep(1.5)
        try :
            self.logFile.close()
        except :
            pass
        #test if the model has been generated 
        generatedModelPath = self.saveDataPath + "." + str(self.maxIte - 1) + ".model"
        if not os.path.exists(generatedModelPath) :
            self.logText.insert(tk.END , "生成模型失败\n" , "head")
            self.trainTipsVar.set("失败")
        else :
            try :
                self.trainTipsVar.set("已完成")
                subprocess.Popen("explorer /select,"+self.saveDataPath + "." + str(self.maxIte - 1) + ".model")
            except :
                pass
        #disabled the text & enable the traint btn
        try :
            self.trainBtn.config(state=tk.NORMAL)
            self.logText.config(state=tk.DISABLED) 
        except :
            pass
        
    def work(self) :
        self.workThread = threading.Thread(target=self.cmdWork , args=(self.cmdstr , ))
        self.isWorkThreadEnd = False
        
        self.logText.config(state=tk.NORMAL)
        self.trainBtn.config(state=tk.DISABLED)
        self.trainTipsVar.set("训练时间较长,请耐心等待,不要关掉程序.")
        
        self.workThread.start()
        threading.Thread(target=self.updateLog).start()
        
    
    def cmdWork(self , cmdstr) :
        self.isWorkThreadEnd = False
        sp = subprocess.Popen(cmdstr , shell=True )
        sp.wait()
        self.isWorkThreadEnd = True 
