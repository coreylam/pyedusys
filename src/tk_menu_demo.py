# -*- coding: utf-8 -*-
from Tkinter import *
import tkMessageBox

    
def alert(msg="Hello"):
    #用于菜单栏调用的函数
    tkMessageBox.showinfo("INFO", msg)
#创建窗口
root = Tk() 
#创建属于root窗口的菜单（Menu）对象，menubar是一整个菜单栏
menubar = Menu(root) 

# 创建菜单栏的一个菜单项（如菜单栏中的 文件、编辑、帮助都是菜单项）
fileMenu = Menu(menubar, tearoff = 0)
fileMenu.add_command(label=u'新建',command = lambda: alert(u"新建文件"))
fileMenu.add_command(label=u'打开',command = lambda: alert(u"打开文件"))

aboutMenu = Menu(menubar, tearoff = 0)
aboutMenu.add_command(label=u'关于', command= lambda:alert(u"这是一个菜单栏的示例程序"))


#在菜单栏中加入菜单
menubar.add_cascade(label=u"文件", menu = fileMenu)
menubar.add_cascade(label=u"关于", menu = aboutMenu)

#在窗体中加入菜单栏
root['menu']=menubar
root.title(u'Menu示例')
root.mainloop()