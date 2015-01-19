#coding=utf8
import Tkinter as tk
import ttk
import webbrowser

from normalConfig import NormalConfig
from normalEventHandler import NormalEventHandler
from generalFunction import *
from toolTips import ToolTip

class Intro(tk.Frame) :
    def __init__(self , master) :
        tk.Frame.__init__(self , master)
        NormalConfig.setUserGrid(self,1,30 ,self.winfo_reqwidth() , self.winfo_reqheight())
        self.gitlink = "https://github.com/HIT-SCIR/ltp-cws" ;
        self.modellink = "http://pan.baidu.com/share/link?shareid=1988562907&uk=2738088569#path=%252Fltp-models%252F3.2.0%252Fsubmodels" ;
        self.createWidgets()
        
    def createWidgets(self) :
        
        self.textPane = createTextWithScroll(self)
        self.textPane.tag_config("li" , font=("Microsoft YaHei" , 12 , "bold") , lmargin1=29 , spacing1=10 , spacing3=10)
        self.textPane.tag_config("text-margin" , lmargin1=29 , lmargin2=5 , spacing2=5 , spacing3=10)
        self.textPane.tag_config("a" , foreground="#0000aa")
        self.textPane.tag_config("sub-title" , font=("Microsoft YaHei" , 8 , "bold"))
        self.textPane.tag_config("href_git")
        self.textPane.tag_config("href_model")
        introPara = [
            "LTP的分词模块基于结构化感知器（Structured Perceptron）算法构建，具有准确率高、速度快等优点；同时支持用户自定义词典，适应不同用户的需求；另外还新增了个性化（增量式）训练功能，用户可以根据自己的实际需求，如对新领域的文本进行分词等，自行标注少量句子的分词结果（比如对LTP分词结果的修正），LTP分词模块可以重新训练一个更好应对新领域的分词器，进一步提高新领域上分词的准确率。" ,
            "分词是许多自然语言处理任务的基础，应用最为广泛。为了方便用户使用分词功能，我们把分词模块独立出来开发了LTP分词版(LTP-CWS)。"
        
        ]
        usagePara = [
            ("训练集和开发集语料格式" ,
            "每行包含一个或几个经过人工切分的句子。人工切分的句子样例如下：\n对外  ， 他们  代表  国家  。"
            ) ,
            ( "基础模型训练" , "本模块用于训练基础模型（推荐使用上述LTP分词模型作为基础模型）。\n选择相应的训练集语料、开发集语料以及模型保存路径，点击训练按钮即开始训练。训练一般耗时较长，请耐心等待。生成的模型保存在模型保存路径指定的位置。" 
            ),
            ("基础模型测试" ,
            "本模块用于测试基础模型。\n选择相应的测试集语料，基础模型路径和输出结果路径，点击测试按钮即开始测试。测试结果保存在输出结果路径指定的位置。"
            ) ,
            (
            "个性化模型训练" ,
            "本模块用于基础模型的基础上训练用户自定义的个性化模型。\n选择相应的训练集语料、开发集语料以及基础模型路径，设置个性化模型保存位置，点击训练按钮即开始训练。训练一般耗时较长，请耐心等待。生成的模型保存在个性化模型保存路径指定的位置。"
            ) ,
            ("个性化模型测试" ,
            "本模块用于测试个性化模型。\n选择测试集语料，指定个性化模型和相应的基础模型，点击测试按钮即开始测试。训练一般耗时较长，请耐心等待。测试结果保存在输出结果路径指定的位置。"
            
            )
        ]
        
        info = "本程序是基于LTPCWS中otcws , otcws-customized程序的GUI外壳，主要用于DEMO演示。\n本程序的稳定性不代表LTPCWS的稳定性。\n"
        #add text
        self.textPane.config(state=tk.NORMAL)
        self.textPane.insert(tk.END , "LTP分词版\n" , "head")
        self.textPane.insert(tk.END ,"简介\n" , "li" )
        for i in range(len(introPara)) :
            self.textPane.insert(tk.END , introPara[i] + "\n", ("cnText" , "text-margin" ,))
        self.textPane.insert(tk.END , "项目\n" , "li")
        self.textPane.insert(tk.END , "github项目托管 : " , ("text-margin","cnText"))
        self.textPane.insert(tk.END , self.gitlink , ("text" , "a" , "href_git"))
        self.textPane.insert(tk.END , "\n")
        self.textPane.insert(tk.END , "分词模型 : " , ("cnText"  , "text-margin"))
        self.textPane.insert(tk.END , "百度云" , ("cnText" , "a" , "href_model" , "text-margin"))
        self.textPane.insert(tk.END , "\n")
        
        self.textPane.insert(tk.END , "使用说明\n" , "li")
        for i in range(len(usagePara)) :
            self.textPane.insert(tk.END , usagePara[i][0] + "\n", ("sub-title" , "text-margin"))
            self.textPane.insert(tk.END , usagePara[i][1] + "\n" , ("cnText" , "text-margin"))
        
        
        self.textPane.insert(tk.END , "关于本程序\n" , "li")
        self.textPane.insert(tk.END , info , ("cnText" , "text-margin"))
        #add link action
        self.textPane.tag_bind("a" , "<Enter>" , lambda e : self.textPane.config(cursor="hand2"))
        self.textPane.tag_bind("a" , "<Leave>" , lambda e : self.textPane.config(cursor="arrow"))
        self.textPane.tag_bind("href_git" , "<Button-1>" , lambda e,link=self.gitlink : webbrowser.open(link))
        self.textPane.tag_bind("href_model" , "<Button-1>" , lambda e,link=self.modellink : webbrowser.open(link))
        
        self.textPane.config(state=tk.DISABLED)