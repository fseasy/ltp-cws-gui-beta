#coding=utf-8

import Tkinter as tk
import ttk
import tkFileDialog
import tkFont

import sys
import os

BASE_PATH = os.path.dirname(os.path.realpath(__file__))
sys.path.append(BASE_PATH)

from subele.basicTrainPanel import BasicTrainPanel
from subele.basicTestPanel import BasicTestPanel
from subele.customTrainPanel import CustomTrainPanel
from subele.customTestPanel import CustomTestPanel
from subele.intro import Intro
from subele.normalConfig import NormalConfig
from subele.normalEventHandler import NormalEventHandler

class LtpwsFrame(tk.Frame) :
    width = 600 
    height = 450
    def __init__(self , master=None) :
        tk.Frame.__init__(self , master)
        self.master.geometry('x'.join([str(self.width),str(self.height)]))
        self.master.resizable(0,0) 
        self.grid(sticky=tk.N+tk.S+tk.W+tk.E)
        self.conf = NormalConfig(self,BASE_PATH)

        self.createWidgets()

    def createWidgets(self) :
        self.notebook = ttk.Notebook(self , width=self.width , height=self.height-30 )
        self.notebook.grid(row=0,column=0,rowspan=10 , columnspan=10,sticky=tk.W+tk.E+tk.N+tk.S)
        self.basicTrainPanel = BasicTrainPanel(self , self.conf)
        self.basicTestPanel = BasicTestPanel(self , self.conf)
        self.customTrainPanel = CustomTrainPanel(self , self.conf)
        self.customTestPanel = CustomTestPanel(self , self.conf)
        self.intro = Intro(self)
        
        self.notebook.add(self.intro , text="简介")
        self.notebook.add(self.basicTrainPanel , text="基础模型训练")
        self.notebook.add(self.basicTestPanel , text="基础模型测试")
        self.notebook.add(self.customTrainPanel , text="个性化模型训练")
        self.notebook.add(self.customTestPanel , text="个性化模型测试")
        

ltpws_gui = LtpwsFrame()
ltpws_gui.master.title("LTP分词版")
try :
    ltpws_gui.master.iconbitmap("ltp_logo.ico")
except :
    pass
ltpws_gui.mainloop()
