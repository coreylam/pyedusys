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
from login_plain import LoginPlain

class MainPlain():

    def __init__(self):
        #创建窗口
        self.login_status = False
        self.student_plain = None
        self.course_plain = None
        self.database_plain = None
        self.login_plain = None
        self.dbc = DatabaseControl()
        self.root = Tk() 
        self.root.protocol('WM_DELETE_WINDOW', self.close)
        #创建属于root窗口的菜单（Menu）对象，menubar是一整个菜单栏
        menubar = Menu(self.root) 

        # 创建菜单栏的一个菜单项（如菜单栏中的 文件、编辑、帮助都是菜单项）
        fileMenu = Menu(menubar, tearoff = 0)
        fileMenu.add_command(label=u'登录',command = self.login)
        fileMenu.add_command(label=u'退出账号',command = self.logout)
        fileMenu.add_command(label=u'关闭',command = self.close)

        ## 关于
        aboutMenu = Menu(menubar, tearoff = 0)
        aboutMenu.add_command(label=u'关于', command= lambda:self.alert(u"这是一个菜单栏的示例程序"))

        ## 管理
        manageMenu = Menu(menubar, tearoff = 0)
        manageMenu.add_command(label=u'管理学生', command= self.manage_student)
        manageMenu.add_command(label=u'管理课程', command= self.manage_course) 
        
        ## 编辑
        editMenu = Menu(menubar, tearoff = 0)
        editMenu.add_command(label=u'数据库', command= self.manage_database)
        editMenu.add_command(label=u'Null', command= self.dbc.print_setting)
        
        #在菜单栏中加入菜单
        menubar.add_cascade(label=u"文件", menu = fileMenu)
        menubar.add_cascade(label=u"管理", menu = manageMenu)
        menubar.add_cascade(label=u"编辑", menu = editMenu)
        menubar.add_cascade(label=u"关于", menu = aboutMenu)

        #在窗体中加入菜单栏
        self.root['menu']=menubar
        self.root.title(u'Menu示例')
        self.root.mainloop()

            
    def top(self, window):
        window.wm_attributes('-topmost',1)
        
    def logout(self):
        if self.login_status :
            self.login_status = False
            self.close_course_plain()
            self.close_student_plain()
            self.alert(u"账号已退出")
        else:
            self.alert(u"当前尚未登录")
        
    def login(self):
        if self.login_status:
            self.alert(u"已登录")
        else:
            # self.alert(u"登录功能开发中")
            # self.manage_login()
            self.login_show()
            
    def login_show(self):
        self.login_windows = Toplevel()
        # self.login_windows.protocol('WM_DELETE_WINDOW', self.destroy)
        self.login_windows.resizable(width=False, height=False)
        label_top = Label(self.login_windows, text=u"用户登录", font=('Arial', 25))
        label_top.grid(row=0, columnspan=3)
        self.login_dict = {}
        self.login_dict['user'] = ""
        self.login_dict['passwd'] = ""
        self.var_user = tk.StringVar()
        self.var_user.set(self.login_dict['user'])
        label_user = Label(self.login_windows, text=u'用户名')
        entry_user = Entry(self.login_windows, textvariable=self.var_user)
        # entry_url.place(x=160, y=150)
        label_user.grid(row=4,column=0)
        entry_user.grid(row=4,column=1, columnspan=2)
        
        self.var_passwd = tk.StringVar()
        self.var_passwd.set(self.login_dict['passwd'])
        label_passwd = Label(self.login_windows, text=u'密码')
        entry_passwd = Entry(self.login_windows, textvariable=self.var_passwd, show="*")
        # entry_url.place(x=160, y=150)
        label_passwd.grid(row=5,column=0)
        entry_passwd.grid(row=5,column=1, columnspan=2)
        
        btn_submit = Button(self.login_windows, text="登录", command = self.check_login)
        btn_cancel = Button(self.login_windows, text="取消", command = self.login_windows.destroy)
        btn_submit.grid(row=6, column=0)
        btn_cancel.grid(row=6, column=2)
        
        self.login_windows.mainloop()
        
    def get_submit_info(self):
        print "submit_info"

        self.login_dict['user'] = self.var_user.get()
        self.login_dict['passwd'] = self.var_passwd.get()
        print self.login_dict
        return 
    
    def check_login(self):
        self.get_submit_info()
        self.login_status = self.dbc.check_account(self.login_dict['user'], self.login_dict['passwd'])
        if self.login_status:
            self.alert(u"登录成功")
            self.login_windows.destroy()
        else:
            self.alert(u"登录失败")
            self.top(self.login_windows)
        
    def alert(self, msg):
        msb = tkMessageBox.showinfo("INFO", msg)
        # msb.wm_attributes('-topmost',1)
        
    def manage_student(self):
        if not self.login_status:
            self.alert(u"请先登录")
            return 
            
        if self.student_plain is not None and self.student_plain.root is not None:
            # self.alert(u"学生管理界面已存在")
            self.student_plain.destroy()
        else:
            self.student_plain = StudentPlain(self.dbc)
        self.student_plain.show()
    
    def close_student_plain(self):
        if self.student_plain is not None and self.student_plain.root is not None:
            self.student_plain.destroy()
            del self.student_plain
            self.student_plain = None
            
    def manage_course(self):
        if not self.login_status:
            self.alert(u"请先登录")
            return
            
        if self.course_plain is not None and self.course_plain.root is not None:
            # self.alert(u"课程管理界面已存在")
            self.course_plain.destroy()
        else:
            self.course_plain = CoursePlain(self.dbc)
        self.course_plain.show()

    def close_course_plain(self):
        if self.course_plain is not None  and self.course_plain.root is not None:
            self.course_plain.destroy()
            del self.course_plain
            self.course_plain = None
            
    def close(self):
        self.close_course_plain()
        self.close_student_plain()
        self.close_database_plain()
        self.root.destroy()
    
    def manage_database(self):
        if self.database_plain is not None and self.database_plain.root is not None:
            # self.alert(u"课程管理界面已存在")
            self.database_plain.destroy()
        else:
            self.database_plain = DatabasePlain(self.dbc)
        self.database_plain.show()
        
    def close_database_plain(self):
        if self.database_plain is not None  and self.database_plain.root is not None:
            self.database_plain.destroy()
            del self.database_plain
            self.database_plain = None

if __name__ == '__main__':
    win = MainPlain()
