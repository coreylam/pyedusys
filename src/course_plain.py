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

class CoursePlain():
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
        
    def show(self):
        # global self.tree
        self.tabel_name = 'course'
        self.root = Tk()
        self.root.protocol('WM_DELETE_WINDOW', self.destroy)
        self.root.resizable(width=False, height=False)
        labeltop = Label(self.root, text=u"课程信息查询", font=('Arial', 25))
        button1 = Button(self.root, text='刷    新', command = self.refresh_item)
        button2 = Button(self.root, text='编    辑', command = self.edit_item)
        button3 = Button(self.root, text='删    除', command = self.delete_item)
        button4 = Button(self.root, text='添    加', command = self.add_item)
        button1.grid(row=2,column=0)
        button2.grid(row=2,column=1)
        button3.grid(row=2,column=2)
        button4.grid(row=2,column=3)
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

        self.refresh_item()
        self.tree.grid(row=3, columnspan=4)
        self.root.mainloop()  
        
    def refresh_item(self):
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
            
    def edit_item(self):
        print "edit_item"
        # if not (locals().has_key('self.tree')):
            # print "self.tree not found"
            # return 
        selected_items = self.tree.selection()
        if not bool(selected_items):
            return 
        temp = self.tree.item(selected_items[0])['values']
        print temp
        self.edit_view(temp,'update')

    def edit_view(self,item_info, action='update'):
        global ev
        ev = Toplevel()
        ev.resizable(width=False, height=False)
        labeltop = Label(ev, text=u"编辑课程信息", font=('Arial', 25))

        self.label_list=[]
        self.var_list =[]
        self.entry_list = []
        row_cnt = len(self.tree["columns"])
        labeltop.grid(row=0, column=0,columnspan=2)
        for i in range(row_cnt):
            self.label_list.append(Label(ev, text = self.tree["columns"][i]))
            self.var_list.append(tk.StringVar())
            self.var_list[i].set(item_info[i])
            self.entry_list.append(Entry(ev, textvariable=self.var_list[i]))
            self.label_list[i].grid(row=i+1,column=0)
            self.entry_list[i].grid(row=i+1,column=1)

        if action == 'update':
            self.entry_list[0]['state']='readonly'

        btn_submit = Button(ev, text="确定", command = lambda:self.submit_course_info(action))
        btn_cancel = Button(ev, text="取消", command = lambda:self.cancel_view(ev))
        btn_submit.grid(row=row_cnt+1, column=0)
        btn_cancel.grid(row=row_cnt+1, column=1)
        ev.mainloop()  
        

    def submit_course_info(self, action):
        course_dict={}
        course_dict['id']       =self.var_list[0].get().strip()
        course_dict['name']     =self.var_list[1].get().strip()
        course_dict['lesson_no']=self.var_list[2].get().strip()
        course_dict['stime']    =self.var_list[3].get().strip()
        course_dict['etime']    =self.var_list[4].get().strip()
        
        
        if "" in course_dict.values():
            print "info invalid"
            return
            
        if not course_dict['id'].startswith('C'):
            print "student id must be starts with C"
            self.alert("Info",u"课程编号必须以大写字符C开头")
            self.top(ev)
            return 
            
        if self.dbc.edit_course_info(course_dict, action):
            print "set success"
            self.refresh_item()
            ev.destroy()
        else:
            print"set %s info failed"%course_dict['id']

    def cancel_view(self,ev):
        ev.destroy()

    def add_item(self):
        self.edit_view(['','','','','',''], action='add')
    
    def delete_item(self):
        # print 'delete_item'
        selected_items = self.tree.selection()
        if not bool(selected_items):
            return 
            
        if not self.yesno(u"Warning", "是否确认删除？"):
            return 
            
        temp = self.tree.item(selected_items[0])['values']
        course_no = temp[0]
        res = self.dbc.get_learn_by_course_id(course_no)
        if bool(res):
            self.alert("Info",u"该课程有学生报名，请先删除对应课程的条目")
            return 
        print course_no
        if self.dbc.delete_course_by_id(course_no):
            # print "set success"
            self.refresh_item()
        else:
            print"delete %s info failed"%course_no
            
    def destroy(self):
        self.root.destroy()
        self.root = None
        
if __name__ == '__main__':
    course = CoursePlain()
    course.show()
        


