#coding=utf-8

import Tkinter as tk
import tkFileDialog
import os

class NormalEventHandler(tk.Frame) :
    @staticmethod
    def openFileDialogAndSetEntryValue(target) :
        path = os.path.normpath(tkFileDialog.askopenfilename())
        target.delete(0,tk.END)
        target.insert(0,path)
    @staticmethod
    def saveasFileDialogAndSetEntryValue(target , defaultextension) :
        path = tkFileDialog.asksaveasfilename(filetypes=[("默认","*"+defaultextension),("其他(手动指定)","*.*")],)
        path = os.path.normpath(path)
        target.delete(0,tk.END)
        target.insert(0,path)
    @staticmethod
    def workAction(target) :
        if target.isRunable() :
            target.work()
