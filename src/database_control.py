# -*- coding: utf-8 -*-
import pickle
import time

import Tkinter as tk
from Tkinter import *
import tkMessageBox
import ttk
import json
import sys
import MySQLdb


class DatabaseControl():
    def __init__(self, host='127.0.0.1', port=3306, user='root', passwd='admin', db_name='db_education', charset='utf8'):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.db_name = db_name
        self.charset = charset
        self.level = 3
        # self.course_info = []
        # self.course_info.append('CourseNO')
        # self.course_info.append('Name')
        # self.course_info.append('')
        # self.course_info.append('')
        # self.course_info.append('')
        # self.course_info.append('')
        # self.course_info.append('')
        self.course_list = []
        
    def refresh_setting(self, db_dict):
        self.host = db_dict['url']
        self.port = db_dict['port']
        self.user = db_dict['user']
        self.passwd = db_dict['passwd']
        self.db_name = db_dict['database_name']
        self.print_setting()
    
    def print_setting(self):
        print "%s,%s,%s,%s,%s"%(self.host,self.port,self.user,self.passwd,self.db_name)
                
    def connect(self):
        try :
            self.conn = MySQLdb.connect(host=self.host, port=int(self.port), user=self.user, passwd=self.passwd, db=self.db_name, charset=self.charset)
            self.cur = self.conn.cursor()
            return True
        except Exception,ex:
            print "connect sql failed"
            return False
            
    
    def close(self):
        self.conn.close()
        
    def get_all_course(self):
        sqlcmd = "select coursenum,name, lessonnum,starttime, endtime from course"
        self.connect()
        if self.cur.execute(sqlcmd) == 0: 
                print "call sql failed"
                self.close()
                return []
        temp = self.cur.fetchone()
        self.course_list = []
        while temp:
            course_dict={}
            course_dict['id']=temp[0]
            course_dict['name']=temp[1]
            course_dict['lesson_no']=temp[2]
            course_dict['stime']=temp[3]
            course_dict['etime']=temp[4] 
            temp = self.cur.fetchone()
            self.course_list.append(course_dict)
        self.close()
        return self.course_list
        
    def get_course_by_id(self, id):
        sqlcmd = "select coursenum,name, lessonnum,starttime, endtime from course where coursenum='%s'"%id
        self.connect()
        if self.cur.execute(sqlcmd) == 0: 
                print "call sql failed"
                self.close()
                return []
        temp = self.cur.fetchone()
        course_dict={}
        course_dict['id']=temp[0]
        course_dict['name']=temp[1]
        course_dict['lesson_no']=temp[2]
        course_dict['stime']=temp[3]
        course_dict['etime']=temp[4] 
        self.close()
        return course_dict
        
    def delete_course_by_id(self, id):
        course_dict = self.get_course_by_id(id)
        if not bool(course_dict):
            print "%s not found"%id
            
            return False
        sqlcmd = "DELETE FROM course WHERE course.coursenum = '%s';"%(id)
        print sqlcmd
        self.connect()
        res = self.cur.execute(sqlcmd)
        self.conn.commit()#插入和更新等操作需要commit才能生效
        time.sleep(0.5)
        
        if res==0:
            print"delete %s info failed"%id
            self.conn.rollback()
            self.close()
            return False
            
        self.close()
        return True
            
    def edit_course_info(self, course_dict, action='update'):
        '''action = 'update'/'add'
        '''
        res = self.get_course_by_id(course_dict['id'])
        if  not bool(res) and action=='update':
            # 更新条目，但条目不存在
            print "%s not found" %course_dict['id']
            return False
        if bool(res) and action=='add':
            # 添加条目，但条目已存在
            print "%s has benn exist"%course_dict['id']
            return False

        self.connect()
        if action == 'add':
        # INSERT INTO `course` (`coursenum`, `name`, `lessonnum`, `starttime`, `endtime`) VALUES ('S1111', 'ddd', 'dfasdf', 'asdfasdf','','')
            sqlcmd = "INSERT INTO course ( coursenum, name, lessonnum, starttime, endtime) VALUES('%s','%s','%s','%s', '%s')"%(course_dict['id'], course_dict['name'], course_dict['lesson_no'], course_dict['stime'], course_dict['etime'])
        elif action == 'update':
        ##UPDATE `teacher` SET `Name` = '小红111' WHERE `teacher`.`TeacherNO` = 'S000002';
            sqlcmd = "UPDATE course SET name='%s', lessonnum='%s', starttime='%s' , endtime='%s' where coursenum='%s'"%( course_dict['name'], course_dict['lesson_no'], course_dict['stime'], course_dict['etime'],course_dict['id'])
        else:
            print "invalid action %s" %action
            self.connect()
            return False
        print sqlcmd
        res = self.cur.execute(sqlcmd)
        self.conn.commit()#插入和更新等操作需要commit才能生效
        time.sleep(0.5)
        if res==0:
            print"set %s info failed"%course_dict['id']
            self.conn.rollback()
            self.close()
            return False
        else:
            print "set success"

        self.close()
        print "submit_info"
        return True
    
    def get_all_student(self):
        sqlcmd = "select studentnum, name, gender, age, pname, phone, lessonnum, accountnum from student"
        self.connect()
        if self.cur.execute(sqlcmd) == 0: 
                print "call sql failed"
                self.close()
                return []
        temp = self.cur.fetchone()
        self.student_list = []
        while temp:
            student_dict={}
            student_dict['id']=temp[0]
            student_dict['name']=temp[1]
            student_dict['gender']=temp[2]
            student_dict['age']=temp[3]
            student_dict['pname']=temp[4] 
            student_dict['phone']=temp[5] 
            student_dict['lessonnum']=temp[6] 
            student_dict['accountnum']=temp[7] 
            temp = self.cur.fetchone()
            self.student_list.append(student_dict)
        self.close()
        return self.student_list
        
    def get_student_by_id(self, id):
        sqlcmd = "select studentnum, name, gender, age, pname, phone, lessonnum, accountnum from student where studentnum='%s'"%id
        self.connect()
        if self.cur.execute(sqlcmd) == 0: 
                print "call sql failed"
                self.close()
                return []
        temp = self.cur.fetchone()
        student_dict={}
        student_dict['id']=temp[0]
        student_dict['name']=temp[1]
        student_dict['gender']=temp[2]
        student_dict['age']=temp[3]
        student_dict['pname']=temp[4] 
        student_dict['phone']=temp[5] 
        student_dict['lessonnum']=temp[6] 
        student_dict['accountnum']=temp[7] 
        self.close()
        return student_dict
        
    def delete_student_by_id(self, id):
        print "in delete_student_by_id"
        student_dict = self.get_student_by_id(id)
        if not bool(student_dict):
            print "%s not found"%id
            return False
        
        sqlcmd = "DELETE FROM student WHERE student.studentnum = '%s';"%(id)
        print sqlcmd
        self.connect()
        res = self.cur.execute(sqlcmd)
        self.conn.commit()#插入和更新等操作需要commit才能生效
        time.sleep(0.5)
        
        if res==0:
            print"delete %s info failed"%id
            self.conn.rollback()
            self.close()
            return False
        
        self.close()
        return True
        
    def edit_student_info(self, student_dict, action='update'):
        '''action = 'update'/'add'
        '''
        res = self.get_student_by_id(student_dict['id'])
        if  not bool(res) and action=='update':
            # 更新条目，但条目不存在
            print "%s not found" %student_dict['id']
            return False
        if bool(res) and action=='add':
            # 添加条目，但条目已存在
            print "%s has benn exist"%student_dict['id']
            return False

        self.connect()
        if action == 'add':
        # INSERT INTO `course` (`coursenum`, `name`, `lessonnum`, `starttime`, `endtime`) VALUES ('S1111', 'ddd', 'dfasdf', 'asdfasdf','','')
            sqlcmd = "INSERT INTO student ( studentnum, name, gender, age, pname, phone, lessonnum, accountnum) VALUES('%s','%s','%s','%s', '%s','%s','%s','%s')"%(student_dict['id'], student_dict['name'], student_dict['gender'], student_dict['age'], student_dict['pname'], student_dict['phone'], student_dict['lessonnum'], student_dict['accountnum'])
        elif action == 'update':
        ##UPDATE `teacher` SET `Name` = '小红111' WHERE `teacher`.`TeacherNO` = 'S000002';
            sqlcmd = "UPDATE INTO student ( studentnum, name, gender, age, pname, phone, lessonnum, accountnum) VALUES('%s','%s','%s','%s', '%s','%s','%s','%s')"%(student_dict['id'], student_dict['name'], student_dict['gender'], student_dict['age'], student_dict['pname'], student_dict['phone'], student_dict['lessonnum'], student_dict['accountnum'])
            sqlcmd = "UPDATE student SET name='%s', gender='%s', age='%s' , pname='%s', phone='%s', lessonnum='%s', accountnum='%s' where studentnum='%s'"%(student_dict['name'], student_dict['gender'], student_dict['age'], student_dict['pname'], student_dict['phone'], student_dict['lessonnum'], student_dict['accountnum'], student_dict['id'])
        else:
            print "invalid action %s" %action
            self.connect()
            return False
        print sqlcmd
        res = self.cur.execute(sqlcmd)
        self.conn.commit()#插入和更新等操作需要commit才能生效
        time.sleep(0.5)
        if res==0:
            print"set %s info failed"%student_dict['id']
            self.conn.rollback()
            self.close()
            return False
        else:
            print "set success"

        self.close()
        print "submit_info"
        return True
        
    def get_all_learn(self):
        sqlcmd = "select learnid,studentnum, coursenum,bookln, finishln,lackln from learn"
        self.connect()
        if self.cur.execute(sqlcmd) == 0: 
                print "call sql failed"
                self.close()
                return []
        temp = self.cur.fetchone()
        self.learn_list = []
        while temp:
            learn_dict={}
            learn_dict['id']=temp[0]
            learn_dict['studentnum']=temp[1]
            learn_dict['coursenum']=temp[2]
            learn_dict['bookln']=temp[3]
            learn_dict['finishln']=temp[4] 
            learn_dict['lackln']=temp[5] 
            temp = self.cur.fetchone()
            self.learn_list.append(learn_dict)
        self.close()
        return self.learn_list
        
    def edit_learn_info(self, learn_dict, action='update'):
        '''action = 'update'/'add'
        '''
        res = self.get_learn_by_id(learn_dict['id'])
        if  not bool(res) and action=='update':
            # 更新条目，但条目不存在
            print "%s not found" %learn_dict['id']
            return False
        if bool(res) and action=='add':
            # 添加条目，但条目已存在
            print "%s has benn exist"%learn_dict['id']
            return False

        self.connect()
        if action == 'add':
        # INSERT INTO `course` (`coursenum`, `name`, `lessonnum`, `starttime`, `endtime`) VALUES ('S1111', 'ddd', 'dfasdf', 'asdfasdf','','')
            sqlcmd = "INSERT INTO learn ( learnid, studentnum, coursenum, bookln, finishln, lackln) VALUES('%s','%s','%s','%s', '%s', %s)"%(learn_dict['id'], learn_dict['studentnum'], learn_dict['coursenum'], learn_dict['bookln'], learn_dict['finishln'], learn_dict['lackln'])
        elif action == 'update':
        ##UPDATE `teacher` SET `Name` = '小红111' WHERE `teacher`.`TeacherNO` = 'S000002';
            sqlcmd = "UPDATE learn SET studentnum='%s', coursenum='%s', bookln='%s' , finishln='%s' , lackln='%s' where learnid='%s'"%( learn_dict['studentnum'], learn_dict['coursenum'], learn_dict['bookln'], learn_dict['finishln'],learn_dict['lackln'],learn_dict['id'])
        else:
            print "invalid action %s" %action
            self.connect()
            return False
        print sqlcmd
        res = self.cur.execute(sqlcmd)
        self.conn.commit()#插入和更新等操作需要commit才能生效
        time.sleep(0.5)
        if res==0:
            print"set %s info failed"%learn_dict['id']
            self.conn.rollback()
            self.close()
            return False
        else:
            print "set success"

        self.close()
        print "submit_info"
        return True
        
    def get_learn_by_id(self, id):
        sqlcmd = "select learnid,studentnum, coursenum,bookln, finishln,lackln from learn where learnid = '%s' "%id

        self.connect()
        if self.cur.execute(sqlcmd) == 0: 
                print "call sql failed"
                self.close()
                return []
        temp = self.cur.fetchone()
        learn_dict={}
        learn_dict['id']=temp[0]
        learn_dict['studentnum']=temp[1]
        learn_dict['coursenum']=temp[2]
        learn_dict['bookln']=temp[3]
        learn_dict['finishln']=temp[4] 
        learn_dict['lackln']=temp[5] 
        self.close()
        return learn_dict

    def delete_learn_by_id(self, id):
        learn_dict = self.get_learn_by_id(id)
        if not bool(learn_dict):
            print "%s not found"%id
            return False
        sqlcmd = "DELETE FROM learn WHERE learn.learnid = '%s';"%(id)
        print sqlcmd
        self.connect()
        res = self.cur.execute(sqlcmd)
        self.conn.commit()#插入和更新等操作需要commit才能生效
        time.sleep(0.5)
        
        if res==0:
            print"delete %s info failed"%id
            self.conn.rollback()
            self.close()
            return False
            
        self.close()
        return True
        
        
        
    def get_learn_by_stud_id(self, id):
        sqlcmd = "select learnid,studentnum, coursenum,bookln, finishln,lackln from learn where studentnum = '%s' "%id

        self.connect()
        if self.cur.execute(sqlcmd) == 0: 
                print "call sql failed"
                self.close()
                return []
        temp = self.cur.fetchone()
        learn_list = []
        while temp:
            learn_dict={}
            learn_dict['id']=temp[0]
            learn_dict['studentnum']=temp[1]
            learn_dict['coursenum']=temp[2]
            learn_dict['bookln']=temp[3]
            learn_dict['finishln']=temp[4] 
            learn_dict['lackln']=temp[5] 
            temp = self.cur.fetchone()
            learn_list.append(learn_dict)
        self.close()
        return learn_list
        
    def get_learn_by_course_id(self, id):
        sqlcmd = "select learnid,studentnum, coursenum,bookln, finishln,lackln from learn where coursenum = '%s' "%id

        self.connect()
        if self.cur.execute(sqlcmd) == 0: 
                print "call sql failed"
                self.close()
                return []
        temp = self.cur.fetchone()
        learn_list = []
        while temp:
            learn_dict={}
            learn_dict['id']=temp[0]
            learn_dict['studentnum']=temp[1]
            learn_dict['coursenum']=temp[2]
            learn_dict['bookln']=temp[3]
            learn_dict['finishln']=temp[4] 
            learn_dict['lackln']=temp[5] 
            temp = self.cur.fetchone()
            learn_list.append(learn_dict)
        self.close()
        return learn_list
        
    def check_account(self, username, password):
        sqlcmd = "select account,password,accountlevel from management where account = '%s'" % username
        
        self.connect()
        if self.cur.execute(sqlcmd) == 0:
                print "call sql failed"
                print sqlcmd
                self.close()
                return []
        temp = self.cur.fetchone()
        self.close()
        self.level = temp[2]
        return temp[1]==password
        
class DatabasePlain():
    def __init__(self, database_control, filename = 'db.conf'):
        self.filename = filename
        self.dbc = database_control
        self.db_dict = {}
        self.db_dict['url'] = "127.0.0.1"
        self.db_dict['port'] = "3306"
        self.db_dict['user'] = "root"
        self.db_dict['passwd'] = "admin"
        self.db_dict['database_name'] = "db_education"
        
    def alert(self, title="Info", msg=""):
        msb = tkMessageBox.showinfo(title, msg)
        
    def top(self, window):
        window.wm_attributes('-topmost',1)
        
    def yesno(self, title="Info", msg=""):
        return tkMessageBox.askyesno(title, msg) 
        
    def destroy(self):
        self.root.destroy()
        self.root = None
        
    def show(self):
        self.root = Toplevel()
        self.root.protocol('WM_DELETE_WINDOW', self.destroy)
        self.root.resizable(width=False, height=False)
        label_top = Label(self.root, text=u"配置数据库信息", font=('Arial', 25))
        label_top.grid(row=0, columnspan=3)
        
        self.load_config()
        self.var_url = tk.StringVar()
        self.var_url.set(self.db_dict['url'])
        label_url = Label(self.root, text=u'数据库网址')
        entry_url = Entry(self.root, textvariable=self.var_url)
        # entry_url.place(x=160, y=150)
        label_url.grid(row=1,column=0)
        entry_url.grid(row=1,column=1, columnspan=2)
        
        self.var_port = tk.StringVar()
        self.var_port.set(self.db_dict['port'])
        label_port = Label(self.root, text=u'数据库端口')
        entry_port = Entry(self.root, textvariable=self.var_port)
        # entry_url.place(x=160, y=150)
        label_port.grid(row=2,column=0)
        entry_port.grid(row=2,column=1, columnspan=2)
        
        self.var_db = tk.StringVar()
        self.var_db.set(self.db_dict['database_name'])
        label_db = Label(self.root, text=u'数据库名称')
        entry_db = Entry(self.root, textvariable=self.var_db)
        # entry_url.place(x=160, y=150)
        label_db.grid(row=3,column=0)
        entry_db.grid(row=3,column=1, columnspan=2)
        
        
        self.var_user = tk.StringVar()
        self.var_user.set(self.db_dict['user'])
        label_user = Label(self.root, text=u'用户名')
        entry_user = Entry(self.root, textvariable=self.var_user)
        # entry_url.place(x=160, y=150)
        label_user.grid(row=4,column=0)
        entry_user.grid(row=4,column=1, columnspan=2)
        
        self.var_passwd = tk.StringVar()
        self.var_passwd.set(self.db_dict['passwd'])
        label_passwd = Label(self.root, text=u'密码')
        entry_passwd = Entry(self.root, textvariable=self.var_passwd, show="*")
        # entry_url.place(x=160, y=150)
        label_passwd.grid(row=5,column=0)
        entry_passwd.grid(row=5,column=1, columnspan=2)
        
        btn_submit = Button(self.root, text="确定", command = self.get_submit_info)
        btn_save = Button(self.root, text="保存", command = self.save_config)
        btn_submit.grid(row=6, column=0)
        btn_save.grid(row=6, column=2)
        
        self.root.mainloop()
        
    def get_submit_info(self):
        print "submit_info"
        self.db_dict = {}
        self.db_dict['url'] = self.var_url.get()
        self.db_dict['port'] = self.var_port.get()
        self.db_dict['user'] = self.var_user.get()
        self.db_dict['passwd'] = self.var_passwd.get()
        self.db_dict['database_name'] = self.var_db.get()
        self.dbc.refresh_setting(self.db_dict)
        print self.db_dict
        return 
    
    def save_config(self):
        fid = open(self.filename, 'w')
        self.get_submit_info()
        js_obj = json.dumps(self.db_dict)
        fid.write(js_obj)
        fid.close()
        
    def load_config(self):
        try:
            fid = open(self.filename, 'r')
            dict_str = fid.read()
            print dict_str
            self.db_dict = json.loads(dict_str)
            return True
        except Exception, ex:
            print "read failed"
            print ex
            return False
if __name__ == "__main__":
    dbc = DatabaseControl()
    # course_list = dbc.get_all_student()
    # for i in course_list:
        # print i
    # student_dict =   dbc.get_student_by_id('S0001')
    # student_dict['name'] =u"里呢酷睿"
    # dbc.edit_student_info(student_dict)
    dbp = DatabasePlain(dbc)
    dbp.show()
    