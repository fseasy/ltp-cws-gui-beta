#coding=utf-8
import Tkinter as tk
import ttk
import tkFileDialog
import tkFont

import os
import sys
import subprocess
import threading
import time

from normalConfig import NormalConfig
from normalEventHandler import NormalEventHandler
from generalFunction import * 

class CustomTrainPanel(ttk.Frame) :
    def __init__(self , master , conf) :
        ttk.Frame.__init__(self , master)
        self.grid_propagate(False)
        NormalConfig.setNormalGrid(self);
        self.conf = conf ;
        
        self.createWidgets()
        
    def createWidgets(self) :
        ttk.Label(self , text="基础模型路径" , font=NormalConfig.cnFont).grid(row=0 , column=0 , columnspan=6 , padx=10 , sticky=tk.W+tk.E)
        self.basicModelEntry = ttk.Entry(self)
        self.basicModelEntry.grid(row=0 , column=6 , columnspan=10 , sticky=tk.W + tk.E)
        self.basicModelBtn = ttk.Button(self, text="浏览" , command=lambda : NormalEventHandler.openFileDialogAndSetEntryValue(self.basicModelEntry))
        self.basicModelBtn.grid(row=0 , column=17 , columnspan=2)
    

        self.trainingDataLabel = ttk.Label(self , text="训练集文件路径" , font=NormalConfig.cnFont)
        self.trainingDataLabel.grid(row=1 , column=0 , columnspan=6,sticky=tk.W+tk.E , padx=10 )
        self.trainingDataEntry = ttk.Entry(self)
        self.trainingDataEntry.grid(row=1 , column=6 , columnspan=10 , sticky=tk.W + tk.E) #padding 1 col
        self.trainingDataBtn = ttk.Button(self , text="浏览" , command=lambda : NormalEventHandler.openFileDialogAndSetEntryValue(self.trainingDataEntry))
        self.trainingDataBtn.grid(row=1 , column=17 , columnspan=2)
        
        self.devDataLabel = ttk.Label(self , text="开发集文件路径" , font=NormalConfig.cnFont) 
        self.devDataLabel.grid(row=2 , column=0 , columnspan=6, padx=10 , sticky=tk.W+tk.E)
        self.devDataEntry = ttk.Entry(self)
        self.devDataEntry.grid(row=2 , column=6 , columnspan=10 , sticky=tk.E+tk.W)
        self.devDataBtn = ttk.Button(self , text="浏览" , command=lambda : NormalEventHandler.openFileDialogAndSetEntryValue(self.devDataEntry))
        self.devDataBtn.grid(row=2 , column=17 , columnspan=2)

        self.saveDataLabel = ttk.Label(self , text="基础模型保存路径" , font=NormalConfig.cnFont)
        self.saveDataLabel.grid(row=3 , column=0 , columnspan=6, padx=10 , sticky=tk.W+tk.E)
        self.saveDataEntry = ttk.Entry(self)
        self.saveDataEntry.grid(row=3 , column=6 , columnspan=10 , sticky=tk.E+tk.W)
        self.saveDataBtn = ttk.Button(self , text="浏览" , command=lambda : NormalEventHandler.saveasFileDialogAndSetEntryValue(self.saveDataEntry))
        self.saveDataBtn.grid(row=3 , column=17 , columnspan=2 )
        
        self.maxIteLabel = ttk.Label(self , text="训练最大迭代次数" , font=NormalConfig.cnFont).grid(row=4,column=0 , columnspan=6 , padx=10 , sticky=tk.W + tk.E )
        self.maxIteEntry = ttk.Entry(self, width=2)
        self.maxIteEntry.grid(row=4 , column=6 , sticky=tk.W + tk.E)
        self.maxIteEntry.insert(0,"5")
   
        self.trainBtn = ttk.Button(self , text="个性化模型训练" )
        self.trainBtn.grid(row=5 , column=0 , columnspan=5 , padx=10 , sticky=tk.W)
