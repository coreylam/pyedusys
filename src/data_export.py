#!/usr/bin/python 
# coding: utf-8

from tkFileDialog import askopenfilename, askdirectory
import Tkinter as tk
from database_control import DatabaseControl
from Tkinter import *
import tkMessageBox
import ttk
import xlwt
import xlrd
import os

class DataFileBase(object):
    """docstring for DataFileBase"""
    def __init__(self, dbc=None, window = None):
        super(DataFileBase, self).__init__()
        self.filetypes=[('datasheet', '*.xlsx'),('datasheet','*.xls'),('datasheet','*.csv'),('allfiles', '*')]
        self.filendir = r"F:/projects/github/pyedusys/src/" 
        self.filename = 'test.xls'


    def open_file(self, parent=None, package=False, initialdir='.'):
        """launch a file browser"""
        filename = ""
        if not package:
            filename = askopenfilename(parent=parent, filetypes=self.filetypes , title='打开文件', initialdir = initialdir)
        else:
            filename = askdirectory(parent=parent, title="打开文件保存目录", mustexist=1, initialdir=initialdir)
        if filename == ():
            filename = ""
        return filename


class DataExport(DataFileBase):
    """docstring for DataExport"""
    def __init__(self, dbc=None, window=None):
        super(DataExport, self).__init__()
        self.dbc = dbc
        self.root = window
        self.course_title = []
        self.save_dir = ""
        self.save_name = "data.xls"
        self.workbook = xlwt.Workbook(encoding = 'utf-8')
        self.student_sheet = self.workbook.add_sheet('student')
        self.course_sheet = self.workbook.add_sheet('course')
        self.time_style = xlwt.XFStyle()
        self.time_style.num_format_str = 'YYYY-MM-DD' # Other options: D-MMM-YY, D-MMM, MMM-YY, h:mm, h:mm:ss, h:mm, h:mm:ss, M/D/YY h:mm, mm:ss, [h]:mm:ss, mm:ss.0
    # def save(self):
    #     # self.path = os.path.join(self.dir_name, self.file_name)
    #     self.workbook.save(self.path)

    def write_student_title(self):
        student_title = ["学号", "学生姓名", "性别", "年龄", "出生日期", "家长姓名", "电话","课时余额","账户余额","备注"]
        self.write_title(self.student_sheet, student_title, 0)

    def write_course_title(self):
        course_title=["编号","名称","课时","开始时间","结束时间"]
        self.write_title(self.course_sheet, course_title, 0)

    def write_title(self, sheet, title, row = 0):
        for i in range(len(title)):
            sheet.write(row, i, title[i])

    def write_student_data(self):
        student_data = self.dbc.get_all_student()
        self.write_student_title()
        ws = self.student_sheet
        # print student_data
        r = 1
        # print len(student_data)
        ws.col(4).width = 3333 # 3333 = 1" (one inch).
        ws.col(6).width = 4444 # 3333 = 1" (one inch).
        for i in range(len(student_data)):
            # print student_data[i]
            # print student_data[i]['id']
            ws.write(i+r, 0, student_data[i]['id'])
            ws.write(i+r, 1, student_data[i]['name'])
            ws.write(i+r, 2, student_data[i]['gender'])
            ws.write(i+r, 3, student_data[i]['age'])
            ws.write(i+r, 4, student_data[i]['birthday'], self.time_style)
            ws.write(i+r, 5, student_data[i]['pname'])
            ws.write(i+r, 6, student_data[i]['phone'])
            ws.write(i+r, 7, student_data[i]['lessonnum'])
            ws.write(i+r, 8, student_data[i]['accountnum'])
            ws.write(i+r, 9, student_data[i]['note'])

    def write_course_data(self):
        course_data = self.dbc.get_all_course()
        # print course_data
        self.write_course_title()
        ws = self.course_sheet
        r = 1
        ws.col(3).width = 3333 # 3333 = 1" (one inch).
        ws.col(4).width = 3333 # 3333 = 1" (one inch).
        for i in range(len(course_data)):
            ws.write(i+r, 0, course_data[i]['id'])
            ws.write(i+r, 1, course_data[i]['name'])
            ws.write(i+r, 2, course_data[i]['lesson_no'])
            ws.write(i+r, 3, course_data[i]['stime'], self.time_style)
            ws.write(i+r, 4, course_data[i]['etime'], self.time_style)

    def run(self):

        self.save_dir = self.var_dir.get().strip()
        self.save_name = self.var_name.get().strip()
        self.write_student_data()
        self.write_course_data()
        self.save_path = os.path.join(self.save_dir, self.save_name)
        self.workbook.save(self.save_path)
        self.root.destroy()

    def get_filepath(self):
        dir_name = self.open_file(self.root, True)
        if dir_name == "":
            dir_name = os.getcwd()
        self.dir_name = dir_name
        # self.save_path = os.path.join(dir_name, "data.xls")
        self.entry_dir.delete(0, END)
        self.entry_dir.insert(END, self.dir_name)

    def show(self):
        # root = tk.Tk()
        root  = self.root 
        txt_font = ('Arial', 12)
        # self.dir_name = self.open_file(self.root, True)

        label_dir = Label(root, text=u'保存文件目录：', font=txt_font)
        label_dir.grid(row=0, column=0)

        self.var_dir = StringVar()
        self.var_dir.set(self.save_dir)
        self.entry_dir = Entry(root, textvariable = self.var_dir, font = txt_font)
        self.entry_dir.grid(row=0, column=1)

        btn_open = Button(root, text='选择目录', command = self.get_filepath, font= txt_font)
        btn_open.grid(row=0, column = 2)

        label_name = Label(root, text=u"保存文件名称：", font = txt_font)
        label_name.grid(row=1, column=0)

        self.var_name = StringVar()
        self.var_name.set(self.save_name)
        self.entry_name = Entry(root, textvariable=self.var_name    , font = txt_font)
        self.entry_name.grid(row=1, column=1)

        btn_save = Button(root, text='保存',command=self.run, font = txt_font)

        btn_save.grid(row=2, column=2)
        root.mainloop()
# 

def main():
    root = tk.Tk()
    dbc = DatabaseControl()
    dfile = DataExport(dbc, root)
    dfile.show()
    root.mainloop()
    # wb = xlwt.Workbook()
    # ws = wb.add_sheet('student')
    # ws.write(0,0,1)
    # style = xlwt.XFStyle()
    # style.num_format_str = 'D-MMM-YY' # Other options: D-MMM-YY, D-MMM, MMM-YY, h:mm, h:mm:ss, h:mm, h:mm:ss, M/D/YY h:mm, mm:ss, [h]:mm:ss, mm:ss.0
    # ws.write(0,1,1,style)
    # wb.save('dddd.xls')
    
if __name__ == '__main__':
    main()
