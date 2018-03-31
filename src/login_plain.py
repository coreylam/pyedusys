#!/usr/bin/python
# -*- coding: utf-8 -*-
import Tkinter as tk
from Tkinter import *
import tkMessageBox
import ttk
# from Tkinter import messagebox  # import this to fix messagebox error
import pickle
import MySQLdb
import time

from course_plain import CoursePlain
from student_plain import StudentPlain
from database_control import DatabaseControl
from database_control import DatabasePlain

class LoginPlain():
    def __init__(self, database_ctrl=None, login_status = False):
        if database_ctrl:
            self.dbc = database_ctrl
        else:
            self.dbc = DatabaseControl()
        self.login_status = login_status
        self.login_dict = {}
        self.login_dict['user'] = ""
        self.login_dict['passwd'] = ""
        
    def alert(self, title="Info", msg=""):
        msb = tkMessageBox.showinfo(title, msg)
        # msb.wm_attributes('-topmost',1)
        
    def top(self, window):
        window.wm_attributes('-topmost',1)
        
    def yesno(self, title="Info", msg=""):
        return tkMessageBox.askyesno(title, msg) 
        
    def destroy(self):
        self.root.destroy()
        print self.login_status
        self.root = None
    def center_window(self, w, h):
        ## 窗口在屏幕中居中
        # get screen width and height
        ws = self.root.winfo_screenwidth()## 获取整个屏幕的分辨率
        hs = self.root.winfo_screenheight()
        # calculate position x, y
        x = (ws/2) - (w/2)   
        y = (hs/2) - (h/2)
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        
    def show(self):
        self.root = Toplevel()
        self.root.protocol('WM_DELETE_WINDOW', self.destroy)
        self.root.maxsize(width=400, height=400)
        self.root.minsize(width=400, height=400)
        self.root.resizable(width=False, height=False)
        label_top = Label(self.root, text=u"用户登录", font=('Arial', 25))
        label_top.place(x=200, y=400)
        label_top.grid(row=0, columnspan=3)

        self.var_user = tk.StringVar()
        self.var_user.set(self.login_dict['user'])
        label_user = Label(self.root, text=u'用户名')
        entry_user = Entry(self.root, textvariable=self.var_user)
        # entry_url.place(x=160, y=150)
        label_user.grid(row=4,column=0)
        entry_user.grid(row=4,column=1, columnspan=2)
        
        self.var_passwd = tk.StringVar()
        self.var_passwd.set(self.login_dict['passwd'])
        label_passwd = Label(self.root, text=u'密码')
        entry_passwd = Entry(self.root, textvariable=self.var_passwd, show="*")
        # entry_url.place(x=160, y=150)
        label_passwd.grid(row=5,column=0)
        entry_passwd.grid(row=5,column=1, columnspan=2)
        
        btn_submit = Button(self.root, text="登录", command = self.check_login)
        btn_save = Button(self.root, text="取消", command = self.destroy)
        btn_submit.grid(row=6, column=0)
        btn_save.grid(row=6, column=2)
        
        self.root.mainloop()
        
    def get_submit_info(self):
        print "submit_info"

        self.login_dict['user'] = self.var_user.get()
        self.login_dict['passwd'] = self.var_passwd.get()
        print self.login_dict
        return 
    
    def check_login(self):
        self.get_submit_info()
        self.login_status = self.dbc.check_account(self.login_dict['user'], self.login_dict['passwd'])
        # if self.login_status:
            
if __name__ == '__main__':
    lp = LoginPlain()
    lp.show()
        