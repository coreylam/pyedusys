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

from database_control import DatabaseControl

class SigninPlain():
    def __init__(self, database_ctrl=None):
        if database_ctrl:
            self.dbc = database_ctrl
        else:
            self.dbc = DatabaseControl()
        
    def alert(self, title="Info", msg=""):
        msb = tkMessageBox.showinfo(title, msg)
        # msb.wm_attributes('-topmost',1)
        
    def top(self, window):
        window.wm_attributes('-topmost',1)
        
    def yesno(self, title="Info", msg=""):
        return tkMessageBox.askyesno(title, msg) 
        
    def select_course_view(self):
        self.root = Tk()
        self.root.protocol('WM_DELETE_WINDOW', self.destroy)
        self.root.resizable(width=False, height=False)
        labeltop = Label(self.root, text=u"选择课程", font=('Arial', 25))
        button1 = Button(self.root, text='刷    新', command = self.refresh_course_item)
        button2 = Button(self.root, text='下 一 步', command = self.signin_view)
        # button3 = Button(self.root, text='删    除', command = self.delete_item)
        # button4 = Button(self.root, text='添    加', command = self.add_item)
        button1.grid(row=3,column=1)
        button2.grid(row=3,column=2)
        # button3.grid(row=2,column=2)
        # button4.grid(row=2,column=3)
        labeltop.grid(row=0, columnspan=4)
        self.tree=ttk.Treeview(self.root, show="headings")#表格  
        self.tree["columns"]=("编号","名称","课时","开始时间","结束时间")  

        self.tree.column("编号",width=80)   #表示列,不显示  
        self.tree.column("名称",width=80)   #表示列,不显示  
        self.tree.column("课时",width=80)  
        self.tree.column("开始时间",width=80)  
        self.tree.column("结束时间",width=80)  
          
        for a_name in self.tree["columns"]:
            self.tree.heading(a_name,text=a_name)  #显示表头  

        self.refresh_course_item()
        self.tree.grid(row=2, columnspan=4)
        self.root.mainloop()  

    def signin_view(self):
        selected_items = self.tree.selection()
        if not bool(selected_items):
            return 
        temp = self.tree.item(selected_items[0])['values']
        # print temp
        self.course_dict={}
        self.course_dict['id']       = temp[0]
        self.course_dict['name']     = temp[1]
        self.course_dict['lesson_no']= temp[2]
        self.course_dict['stime']    = temp[3]
        self.course_dict['etime']    = temp[4]
        self.root.destroy()
        # self.roo
        self.root = Tk()
        self.root.protocol('WM_DELETE_WINDOW', self.destroy)
        self.root.resizable(width=False, height=False)

        label_top = Label(self.root, text=u"点名", font=('Arial', 25))
        label_top.grid(row=0, columnspan=4)

        label_cid = Label(self.root, text=u"课程编号:")
        label_cid_v = Label(self.root, text=self.course_dict['id'])
        label_cname = Label(self.root, text=u"课程名称:")
        label_cname_v = Label(self.root, text=self.course_dict['name'])
        label_cid.grid(row=1, column=0)
        label_cid_v.grid(row=1, column=1)
        label_cname.grid(row=1, column=2)
        label_cname_v.grid(row=1, column=3)

        btn_singin = Button(self.root, text="签    到", command = self.signin)
        btn_singin_c = Button(self.root, text="取消签到", command = lambda:self.signin('minus'))
        btn_singin.grid(row=3, column=0)
        btn_singin_c.grid(row=3, column=1)

        btn_lack = Button(self.root, text="请    假", command = self.signlack)
        btn_lack_c = Button(self.root, text="取消请假", command = lambda:self.signlack('minus'))
        btn_lack.grid(row=3, column=2)
        btn_lack_c.grid(row=3, column=3)

        self.tree=ttk.Treeview(self.root, show="headings")#表格  
        self.tree["columns"]=("编号", "学号","姓名","已预约课时","已完成课时","请假课时") 
        

        for a_name in self.tree["columns"]:
            self.tree.column(a_name,width=80)  
            self.tree.heading(a_name,text=a_name)  #显示表头  

        self.refresh_learn_item()
        self.tree.grid(row=2, columnspan=4)

        self.root.mainloop()

    def refresh_course_item(self):
        try: 
            slist = self.dbc.get_all_course()
            self.tree.delete(*self.tree.get_children())
            for alist in slist:
                # course_dict={}
                # course_dict['id']=temp[0]
                # course_dict['name']=temp[1]
                # course_dict['lesson_no']=temp[2]
                # course_dict['stime']=temp[3]
                # course_dict['etime']=temp[4] 
                temp=(alist['id'],alist['name'],alist['lesson_no'],alist['stime'],alist['etime'])
                self.tree.insert("",0,values=temp) #插入数据
        except Exception, ex:
            print "get sql data error"
            print ex
            self.alert("ERROR", ex)

    def refresh_learn_item(self):
        try: 
            # print self.course_dict['id']
            learn_list = self.dbc.get_learn_by_course_id(self.course_dict['id'])
            # print learn_list
            self.tree.delete(*self.tree.get_children())
            for alist in learn_list:
                # self.tree["columns"]=("编号","学号","姓名","已预约课时","已完成课时","请假课时")  
                # print alist['studentnum']
                slist = self.dbc.get_student_by_id(alist['studentnum'])
                # print slist
                temp=(alist['id'], alist['studentnum'],slist['name'],alist['bookln'],alist['finishln'],alist['lackln'])
                self.tree.insert("",0,values=temp) #插入数据
        except Exception, ex:
            print "get sql data error"
            print ex
            self.alert("ERROR", ex)

    def signin(self, action = 'add'):
        # action = 'add'/'minus'
        print "signin"
        selected_items = self.tree.selection()
        if not bool(selected_items):
            return 
        for one_item in selected_items:
            lid = self.tree.item(one_item)['values'][0]
            learn_dict = self.dbc.get_learn_by_id(lid)
            if action == 'add':
                learn_dict['finishln'] += 1
            elif action == 'minus':
                learn_dict['finishln'] -= 1
            # print learn_dict
            self.dbc.edit_learn_info(learn_dict,'update')
        self.refresh_learn_item()

    def signlack(self, action = 'add'):
        # action = 'add'/'minus'
        selected_items = self.tree.selection()
        if not bool(selected_items):
            return 
        for one_item in selected_items:
            lid = self.tree.item(one_item)['values'][0]
            learn_dict = self.dbc.get_learn_by_id(lid)
            if action == 'add':
                learn_dict['lackln'] += 1
            elif action == 'minus':
                learn_dict['lackln'] -= 1
            # print learn_dict
            self.dbc.edit_learn_info(learn_dict,'update')
        self.refresh_learn_item()

    def show(self):
        self.select_course_view()

    def destroy(self):
        self.root.destroy()
        self.root = None
        
if __name__ == '__main__':
    signin = SigninPlain()
    signin.show()
        


