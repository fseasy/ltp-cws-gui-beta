#coding=utf-8

import Tkinter as tk
import tkFileDialog
import os

class NormalEventHandler(tk.Frame) :
    @staticmethod
    def openFileDialogAndSetEntryValue(target) :
        path = os.path.normpath(tkFileDialog.askopenfilename())
        if path != '' and path != ".":
            target.delete(0,tk.END)
            target.insert(0,path)
    @staticmethod
    def saveasFileDialogAndSetEntryValue(target , setdefault=False , defaultextension='') :
        path = ""
        if setdefault :
            path = tkFileDialog.asksaveasfilename(defaultextension=defaultextension,filetypes=[("默认","*"+defaultextension),("其他(手动指定)","*.*")],)
        else :
            path = tkFileDialog.asksaveasfilename(filetypes=[("输出模型自动添加后缀.model","*.*")],)
        if path != "" and path != "." :
            path = os.path.normpath(path)
            target.delete(0,tk.END)
            target.insert(0,path)
    @staticmethod
    def workAction(target) :
        if target.isRunable() :
            target.work()
