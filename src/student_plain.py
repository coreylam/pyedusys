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

class StudentPlain():
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
        self.tabel_name = 'student'
        self.root = Tk()
        self.root.protocol('WM_DELETE_WINDOW', self.destroy)
        # root.maxsize(80*8,650)
        # root.minsize(80*8,650)
        self.root.resizable(width=False, height=False)
        labeltop = Label(self.root, text=u"学生信息查询", font=('Arial', 25))
        button1 = Button(self.root, text='刷    新', command = self.refresh_item)
        button2 = Button(self.root, text='编    辑', command = self.edit_item)
        button3 = Button(self.root, text='删    除', command = self.delete_item)
        button4 = Button(self.root, text='添    加', command = self.add_item)
        button5 = Button(self.root, text='报    名', command = self.sign_up)
        button6 = Button(self.root, text='在学课程', command = self.learn_course)
        button1.grid(row=2,column=0)
        button2.grid(row=2,column=1)
        button3.grid(row=2,column=2)
        button4.grid(row=2,column=3)
        button5.grid(row=4,column=0)
        button6.grid(row=4,column=1)
        labeltop.grid(row=0, columnspan=4)

        self.tree=ttk.Treeview(self.root, show="headings")#表格  
        self.tree["columns"]=("学号","姓名","性别", '年龄', '出生日期', '家长姓名', '电话', '课时余额', "账户余额","备注")  

        self.tree.column("学号",width=50)   #表示列,不显示  
        self.tree.column("姓名",width=50)   #表示列,不显示  
        self.tree.column("性别",width=50)  
        self.tree.column("年龄",width=50)  
        self.tree.column("出生日期",width=80)  
        self.tree.column("家长姓名",width=80)  
        self.tree.column("电话",width=80)  
        self.tree.column("课时余额",width=80)  
        self.tree.column("账户余额",width=80)  
        self.tree.column("备注",width=120)  
          
        for a_name in self.tree["columns"]:
            self.tree.heading(a_name,text=a_name)  
        
        self.refresh_item()
        self.tree.grid(row=3, columnspan=4)
        self.root.mainloop()  

    def refresh_item(self):
        try: 
            slist = self.dbc.get_all_student()
            self.tree.delete(*self.tree.get_children())
            for alist in slist:
                # student_dict['id']=temp[0]
                # student_dict['name']=temp[1]
                # student_dict['gender']=temp[2]
                # student_dict['age']=temp[3]
                # student_dict['pname']=temp[4] 
                # student_dict['phone']=temp[5] 
                # student_dict['lessonnum']=temp[6] 
                # student_dict['accountnum']=temp[7] 
                temp=(alist['id'],alist['name'],alist['gender'],alist['age'],alist['birthday'],alist['pname'],alist['phone'],alist['lessonnum'],alist['accountnum'],alist['note'])
                self.tree.insert("",0,values=temp) #插入数据，  
            # self.tree.grid(row=3, columnspan=4)
        except Exception, ex:
            print "get sql data error"
            print ex
            self.alert("ERROR", ex)
            
    def edit_item(self):
        print "edit_item"
        selected_items = self.tree.selection()
        if not bool(selected_items):
            return 
        temp = self.tree.item(selected_items[0])['values']
        print temp
        # student_no = str(temp[0])
        # name = temp[1]
        # gender = temp[2]
        # phone = temp[3]
        # print "%s, %s, %s, %s"%(student_no, name, gender, phone)
        self.edit_view(temp,'update')

    def edit_view(self,item_info, action='update'):
        global ev
        # 这里如果用Tk的话，与root松耦合， 无法在submit_student_info中实时更新var_sno等值（这个问题我调了一个下午）
        ev = Toplevel()
        # ev.maxsize(880,800)
        # ev.minsize(250,230)
        ev.resizable(width=False, height=False)
        labeltop = Label(ev, text=u"编辑学生信息", font=('Arial', 25))
        # self.tree["columns"]=("编号","名称","课时","费用","开始时间","结束时间")  
        
        self.label_list=[]
        self.var_list =[]
        self.entry_list = []
        row_cnt = len(self.tree["columns"])
        # print row_cnt
        labeltop.grid(row=0, column=0,columnspan=2)
        for i in range(row_cnt):
            self.label_list.append(Label(ev, text = self.tree["columns"][i]))
            self.var_list.append(tk.StringVar())
            self.var_list[i].set(item_info[i])
            self.entry_list.append(Entry(ev, textvariable=self.var_list[i]))
            self.label_list[i].grid(row=i+1,column=0)
            self.entry_list[i].grid(row=i+1,column=1)

            
        self.entry_list[3]['state']='readonly'
        if action == 'update':
            self.entry_list[0]['state']='readonly'
        # 设置entry默认值， 改用StringVar + textvariable
        # entry_sno.insert(END, str(item_info[0]))
        # entry_name.insert(END, item_info[1])
        # entry_gender.insert(END, item_info[2])
        # entry_phone.insert(END, item_info[3])
        

        btn_submit = Button(ev, text="确定", command = lambda:self.submit_student_info(action))
        btn_cancel = Button(ev, text="取消", command = lambda:self.cancel_view(ev))
        btn_submit.grid(row=row_cnt+1, column=0)
        btn_cancel.grid(row=row_cnt+1, column=1)
        ev.mainloop()  
        
    def cancel_view(self,ev):
        ev.destroy()

    def submit_student_info(self, action):
        student_dict={}
        student_dict['id']=self.var_list[0].get().strip()
        student_dict['name']=self.var_list[1].get().strip()
        student_dict['gender']=self.var_list[2].get().strip()
        student_dict['age']=self.var_list[3].get().strip()
        student_dict['birthday']=self.var_list[4].get().strip()
        student_dict['pname']=self.var_list[5].get().strip()
        student_dict['phone']=self.var_list[6].get().strip()
        student_dict['lessonnum']=self.var_list[7].get().strip()
        student_dict['accountnum']=self.var_list[8].get().strip()
        student_dict['note']=self.var_list[9].get().strip()
        
        
        if "" in student_dict.values():
            print "info invalid"
            self.alert("Info", u"信息未填写完整，请完整填写所有信息")
            return
            
        if not student_dict['id'].startswith('S'):
            print "student id must be starts with S"
            self.alert("Info",u"学号必须以大写字符S开头")
            self.top(ev)
            return 
            
        if self.dbc.edit_student_info(student_dict, action):
            print "set success"
            self.refresh_item()
            ev.destroy()
        else:
            print"set %s info failed"%student_dict['id']
           
        print "submit_student_info"
        
    def add_item(self):
        self.edit_view(['','','','0','','','','','',''], action='add')
        
    def delete_item(self):
        print 'delete_item'
        selected_items = self.tree.selection()
        if not bool(selected_items):
            return 
            
        if not self.yesno(u"Warning", "是否确认删除？"):
            return 
            
        temp = self.tree.item(selected_items[0])['values']
        student_no = temp[0]
        res = self.dbc.get_learn_by_stud_id(student_no)
        if bool(res):
            self.alert("Info",u"该学生有在学课程，请先删除报名课程")
            return 
        print student_no
        if self.dbc.delete_student_by_id(student_no):
            print "set success"
            self.refresh_item()
        else:
            print"delete %s info failed"%student_no

    def sign_up(self):
        print "sign_up"
        selected_items = self.tree.selection()
        if not bool(selected_items):
            print "no item selected"
            return 
        temp = self.tree.item(selected_items[0])['values']
        student_no = str(temp[0])
        self.sign_up_student_info = self.dbc.get_student_by_id(student_no)
        self.sign_up_course_view()

    def get_course_tree(self, window):
        tree=ttk.Treeview(window, show="headings")#表格  
        tree["columns"]=("编号","名称","总课时","开始时间","结束时间")  

        tree.column("编号",width=80)   #表示列,不显示  
        tree.column("名称",width=100)   #表示列,不显示  
        tree.column("总课时",width=50)  
        tree.column("开始时间",width=170)  
        tree.column("结束时间",width=170)  
        for a_name in tree["columns"]:
            tree.heading(a_name,text=a_name)  #显示表头  
        return tree

    def sign_up_course_view(self, last_window = None):
        ''' The view of SignUP Step1, must be call by sign_up 
        '''
        if bool(last_window):
            self.cancel_view(last_window)
        print "sign_up_course_view"
        # global sign_up_view
        sign_up_view = Toplevel()
        # sign_up_view.maxsize(740,400)
        # sign_up_view.minsize(740,400)
        sign_up_view.resizable(width=False, height=False)
        labeltop = Label(sign_up_view, text=u"选择报名课程", font=('Arial', 25))
        label_sid_info = Label(sign_up_view, text=u"学号")
        label_sid = Label(sign_up_view, text=self.sign_up_student_info['id'])
        label_sname_info = Label(sign_up_view, text=u"姓名")
        label_sname = Label(sign_up_view, text=self.sign_up_student_info['name'])
        button_next = Button(sign_up_view, text = "下一步", command=lambda:self.sign_up_charge_view(sign_up_view, course_tree))
        button_pre = Button(sign_up_view, text = "上一步", command=lambda:self.cancel_view(sign_up_view))
        
        labeltop.grid(row=0, column=0, columnspan=4)
        label_sid_info.grid(row=1,column=0)
        label_sid.grid(row=1,column=1)
        label_sname_info.grid(row=1,column=2)
        label_sname.grid(row=1,column=3)
        button_pre.grid(row=3, column=1)
        button_next.grid(row=3, column=2)
        
        course_tree = self.get_course_tree(sign_up_view)
        course_tree.grid(row=2, column=0, columnspan=4)
        course_list = self.dbc.get_all_course()
        # course_dict={}
        # course_dict['id']=temp[0]
        # course_dict['name']=temp[1]
        # course_dict['lesson_no']=temp[2]
        # course_dict['stime']=temp[3]
        # course_dict['etime']=temp[4] 
        for course_dict in course_list:
        #  {'id', 'name','lesson_no','charge','stime','etime'}
            temp = (course_dict['id'],course_dict['name'],course_dict['lesson_no'],\
            course_dict['stime'],course_dict['etime'])
            course_tree.insert("",0,values=temp)
        self.refresh_item()

    def sign_up_charge_view(self, last_window, course_tree):
        print "sign_up_charge_view"
        selected_items = course_tree.selection()
        if not bool(selected_items):
            print "no item selected"
            return 
        temp = course_tree.item(selected_items[0])['values']
        ## print temp
        course_no = str(temp[0])
        self.sign_up_course_list = self.dbc.get_course_by_id(course_no)
        self.cancel_view(last_window)
        # print self.sign_up_info
        sign_up_charge_window = Toplevel()
        # sign_up_charge_window.maxsize(280,250)
        # sign_up_charge_window.minsize(280,250)
        sign_up_charge_window.resizable(width=False, height=False)
        label_top = Label(sign_up_charge_window, text=u"预约课时信息", font=('Arial', 25))
        label_top.grid(row=0, column=0, columnspan=3)
        
        label_sid_info = Label(sign_up_charge_window, text=u"学号")
        entry_sid = Entry(sign_up_charge_window)
        entry_sid.insert(END, self.sign_up_student_info['id'])
        entry_sid['state'] = 'readonly'
        label_sid_info.grid(row=1, column=0)
        entry_sid.grid(row=1, column=1)
        
        label_sname_info = Label(sign_up_charge_window, text=u"姓名")
        entry_sname = Entry(sign_up_charge_window)
        entry_sname.insert(END, self.sign_up_student_info['name'])
        entry_sname['state'] = 'readonly'
        label_sname_info.grid(row=2, column=0)
        entry_sname.grid(row=2, column=1)
        
        label_ln_info = Label(sign_up_charge_window, text=u"剩余课时")
        entry_ln = Entry(sign_up_charge_window)
        entry_ln.insert(END, self.sign_up_student_info['lessonnum'])
        entry_ln['state'] = 'readonly'
        label_ln_info.grid(row=3, column=0)
        entry_ln.grid(row=3, column=1)
        
        label_cid_info = Label(sign_up_charge_window, text=u"课程编号")
        entry_cid = Entry(sign_up_charge_window)
        entry_cid.insert(END, self.sign_up_course_list['id'])
        entry_cid['state'] = 'readonly'
        label_cid_info.grid(row=4, column=0)
        entry_cid.grid(row=4, column=1)
        
        label_cname_info = Label(sign_up_charge_window, text=u"课程名称")
        entry_cname = Entry(sign_up_charge_window)
        entry_cname.insert(END, self.sign_up_course_list['name'])
        entry_cname['state'] = 'readonly'
        label_cname_info.grid(row=5, column=0)
        entry_cname.grid(row=5, column=1)
        
        label_cln_info = Label(sign_up_charge_window, text=u"课程总课时")
        entry_cln = Entry(sign_up_charge_window)
        entry_cln.insert(END, self.sign_up_course_list['lesson_no'])
        entry_cln['state'] = 'readonly'
        label_cln_info.grid(row=6, column=0)
        entry_cln.grid(row=6, column=1)
        
        self.sign_up_book_ln_var = tk.StringVar()
        label_bln_info = Label(sign_up_charge_window, text=u"预约课时")
        entry_bln = Entry(sign_up_charge_window, textvariable=self.sign_up_book_ln_var)
        entry_bln.insert(END, '0')
        label_bln_info.grid(row=7, column=0)
        entry_bln.grid(row=7, column=1)
        
        button_pre = Button(sign_up_charge_window, text = "上一步", command=lambda: self.sign_up_course_view(sign_up_charge_window))
        button_next = Button(sign_up_charge_window, text = "确定", command=lambda:self.update_bookinglist(sign_up_charge_window))
        button_pre.grid(row=8,column=0)
        button_next.grid(row=8,column=1)
        
    def update_bookinglist(self,last_window):
        print "update_bookinglist"
        book_ln = self.sign_up_book_ln_var.get()
        print book_ln
        org_ln = self.sign_up_student_info['lessonnum']
        new_ln = int(org_ln) - int(book_ln)
        if new_ln<0:
            print "lesson is not enough"
            self.alert('Info',u'该学生剩余课时不足')
            self.top(last_window)
            return 
            
        self.sign_up_student_info['lessonnum']  = str(new_ln)
        if self.dbc.edit_student_info(self.sign_up_student_info, 'update'):
            print "update user info success"
        else :
            print "update user info failed"
            return 
        learn_dict={}
        learn_dict['id']="L%s%s"%(self.sign_up_student_info['id'][1:],self.sign_up_course_list['id'][1:])
        learn_dict['studentnum']=self.sign_up_student_info['id']
        learn_dict['coursenum']=self.sign_up_course_list['id']
        learn_dict['bookln']=str(book_ln)
        learn_dict['finishln']=str(0)
        learn_dict['lackln']=str(0)
        if self.dbc.edit_learn_info(learn_dict,'add'):
            print "add learning schedule success"
            self.cancel_view(last_window)
            self.refresh_item()
        else:
            print "add learning schedule failed"
            self.sign_up_student_info['lessonnum']  = str(org_ln)
            self.dbc.edit_student_info(self.sign_up_student_info, 'update')
            self.alert('Info',u'课程添加失败')
            self.top(last_window)
        
    def learn_course(self):
        selected_items = self.tree.selection()
        if not bool(selected_items):
            return 
        self.select_tree = selected_items
        # temp = self.tree.item(selected_items[0])['values']
        # student_no = str(temp[0])
        # learn_list = self.dbc.get_learn_by_stud_id(student_no)
        # self.learn_course_window(learn_list)
        self.learn_course_window_new(selected_items)
        
    def get_learn_tree(self, window):
        tree=ttk.Treeview(window, show="headings")#表格  
        tree["columns"]=("序号","学号","学生姓名","课程编号","课程名称","已预约课时","已完成课时", "请假课时")  

        tree.column("序号",width=80)   #表示列,不显示  
        tree.column("学号",width=80)   #表示列,不显示  
        tree.column("学生姓名",width=80)  
        tree.column("课程编号",width=80)  
        tree.column("课程名称",width=80)  
        tree.column("已预约课时",width=80)  
        tree.column("已完成课时",width=80)  
        tree.column("请假课时",width=80)  
        for a_name in tree["columns"]:
            tree.heading(a_name,text=a_name)  #显示表头  
        self.learn_tree = tree
        return tree
        
    def learn_course_window(self, learn_list, last_window = None):
    
        if bool(last_window):
            self.cancel_view(last_window)
            
        learn_course_view = Toplevel()
        learn_course_view.resizable(width=False, height=False)
        labeltop = Label(learn_course_view, text=u"课时信息查询", font=('Arial', 25))
        labeltop.grid(row=0,column=0,columnspan=4)
        # label_sid_info = Label(learn_course_view, text=u"学号")
        # label_sid = Label(learn_course_view, text=learn_list['id'])
        # label_sname_info = Label(learn_course_view, text=u"姓名")
        # label_sname = Label(learn_course_view, text=learn_list['name'])
        self.get_learn_tree(learn_course_view)
        learn_tree = self.learn_tree
        learn_tree.grid(row=2, column=0, columnspan=4)
        if bool(learn_list):
            student_info = self.dbc.get_student_by_id(learn_list[0]['studentnum'])
            for learn_dict in learn_list:
                course_info = self.dbc.get_course_by_id(learn_dict['coursenum'])
            # tree["columns"]=("序号", "学号", "学生姓名", "课程编号", "课程名称", "已预约课时", "已完成课时", "请假课时")  
            #  {'id', 'name','lesson_no','charge','stime','etime'}
                # print learn_dict['id'], learn_dict['studentnum'], student_info['name'], learn_dict['coursenum'], course_info['name'], learn_dict['bookln'], learn_dict['finishln'], learn_dict['lackln']
                temp = (learn_dict['id'], learn_dict['studentnum'], student_info['name'], learn_dict['coursenum'], course_info['name'], learn_dict['bookln'], learn_dict['finishln'], learn_dict['lackln'])
                learn_tree.insert("",0,values=temp)
        self.refresh_item()

    def learn_course_window_new(self, selected_items, last_window = None):
    
        if bool(last_window):
            self.cancel_view(last_window)
            
        self.learn_course_view = Toplevel()
      
        self.learn_course_view.resizable(width=False, height=False)
        labeltop = Label(self.learn_course_view, text=u"课时信息查询", font=('Arial', 25))
        labeltop.grid(row=0,column=0,columnspan=4)

        self.get_learn_tree(self.learn_course_view)
        self.learn_tree.grid(row=2, column=0, columnspan=4)

        # button1 = Button(self.learn_course_view, text='刷    新', command = self.refresh_learn_item)
        button1 = Button(self.learn_course_view, text='编    辑', command = lambda: self.edit_learn_item())
        button2 = Button(self.learn_course_view, text='删    除', command = lambda: self.delete_learn_item())
        button1.grid(row=3,column=1)
        button2.grid(row=3,column=2)
        # button3.grid(row=1,column=2)

        self.learn_select_students = []
        # self.refresh_learn_item(selected_items, learn_tree)
        for sitem in selected_items:
            # print sitem
            temp = self.tree.item(sitem)['values']
            # print temp
            student_no = str(temp[0])
            if student_no not in self.learn_select_students:
                self.learn_select_students.append(student_no)
        self.refresh_learn_item()
        self.refresh_item()
    
    def refresh_learn_item(self):
        print "refresh_learn_item"
        # self.selected_items
        # self.alert(msg="refresh_learn_item")
        try: 
            slist = self.dbc.get_all_student()
            self.learn_tree.delete(*self.learn_tree.get_children())
            for student_no in self.learn_select_students:
                learn_list = self.dbc.get_learn_by_stud_id(student_no)
                if not bool(learn_list):
                    continue
                student_info = self.dbc.get_student_by_id(learn_list[0]['studentnum'])
                for learn_dict in learn_list:
                    course_info = self.dbc.get_course_by_id(learn_dict['coursenum'])
                # tree["columns"]=("序号", "学号", "学生姓名", "课程编号", "课程名称", "已预约课时", "已完成课时", "请假课时")  
                #  {'id', 'name','lesson_no','charge','stime','etime'}
                    # print learn_dict['id'], learn_dict['studentnum'], student_info['name'], learn_dict['coursenum'], course_info['name'], learn_dict['bookln'], learn_dict['finishln'], learn_dict['lackln']
                    temp_dict = (learn_dict['id'], learn_dict['studentnum'], student_info['name'], learn_dict['coursenum'], course_info['name'], learn_dict['bookln'], learn_dict['finishln'], learn_dict['lackln'])
                    self.learn_tree.insert("",0,values=temp_dict)
        except Exception, ex:
            print "get sql data error"
            print ex
            self.alert("ERROR", ex)
        
    def edit_learn_view(self, item_info, action='update'):
        print "edit_learn_view"
        self.learn_edit_view = Toplevel()
        self.learn_edit_view.resizable(width=False, height=False)
        labeltop = Label(self.learn_edit_view, text=u"编辑课时信息", font=('Arial', 25))
        self.label_list=[]
        self.var_list =[]
        self.entry_list = []
        title = self.learn_tree["columns"]
        row_cnt = len(title)
        print row_cnt
        labeltop.grid(row=0, column=0,columnspan=2)
        for i in range(row_cnt):
            self.label_list.append(Label(self.learn_edit_view, text = title[i]))
            self.var_list.append(tk.StringVar())
            self.var_list[i].set(item_info[i])
            self.entry_list.append(Entry(self.learn_edit_view, textvariable=self.var_list[i]))
            self.label_list[i].grid(row=i+1,column=0)
            self.entry_list[i].grid(row=i+1,column=1)

            
        if action == 'update':
            self.entry_list[0]['state']='readonly'
            self.entry_list[1]['state']='readonly'
            self.entry_list[2]['state']='readonly'
            self.entry_list[3]['state']='readonly'
            self.entry_list[4]['state']='readonly'
            self.entry_list[5]['state']='readonly'
        # 设置entry默认值， 改用StringVar + textvariable
        # entry_sno.insert(END, str(item_info[0]))
        # entry_name.insert(END, item_info[1])
        # entry_gender.insert(END, item_info[2])
        # entry_phone.insert(END, item_info[3])
        

        btn_submit = Button(self.learn_edit_view, text="确定", command = lambda:self.submit_learn_info(action))
        btn_cancel = Button(self.learn_edit_view, text="取消", command = lambda:self.cancel_view(self.learn_edit_view))
        btn_submit.grid(row=row_cnt+1, column=0)
        btn_cancel.grid(row=row_cnt+1, column=1)
        self.learn_edit_view.mainloop()  
    
    def edit_learn_item(self):
        print "edit_learn_item"
        learn_tree = self.learn_tree
        selected_items = learn_tree.selection()
        if not bool(selected_items):
            return 
        item_info = learn_tree.item(selected_items[0])['values']
        print item_info
        self.edit_learn_view(item_info, action='update')
        
    def delete_learn_item(self):
        print "delete_learn_item"
        learn_tree = self.learn_tree
        sel_learn_item = learn_tree.selection()
        if not bool(sel_learn_item):
            ## 如果选中删除条目，不做任何操作，返回
            print "no item selected"
            return 
            
        if not self.yesno(u"Warning", "是否确认删除？"):
            #窗口置顶
            self.top(self.learn_course_view)
            return 
        for one_item in sel_learn_item:
            temp = learn_tree.item(one_item)['values'] 
            learn_id = str(temp[0]) 
            self.dbc.delete_learn_by_id(learn_id)
        self.refresh_learn_item()
        
    def submit_learn_info(self, action="update"):
        print "submit_learn_info"
        learn_dict={}
        learn_dict['id']=self.var_list[0].get().strip()
        learn_dict['studentnum']=self.var_list[1].get().strip()
        learn_dict['coursenum']=self.var_list[3].get().strip()
        learn_dict['bookln']=self.var_list[5].get().strip()
        learn_dict['finishln']=self.var_list[6].get().strip()
        learn_dict['lackln']=self.var_list[7].get().strip()
        # tree["columns"]=("序号", "学号", "学生姓名", "课程编号", "课程名称", "已预约课时", "已完成课时", "请假课时")  
        
        if "" in learn_dict.values():
            print "info invalid"
            return
            
        if self.dbc.edit_learn_info(learn_dict, action):
            print "set success"
            self.refresh_learn_item()
            self.learn_edit_view.destroy()
        else:
            print"set %s info failed"%learn_dict['id']
           
        print "submit_student_info"
    def destroy(self):
        self.root.destroy()
        self.root = None
        
if __name__ == '__main__':
    stud = StudentPlain()
    stud.show()
        


