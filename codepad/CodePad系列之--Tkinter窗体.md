CodePad系列之--Tkinter窗体
===

Codepad系列是将自己用过的一些小功能代码段记录下来，便于后续查找使用，是一个代码备忘录系列。

本文简单记录在用Tkinter开发GUI窗体时一些简单的代码段，以便后续使用。[官方文档地址](https://docs.python.org/2/library/tkinter.html)
<!--more-->
Hello world
---
任务： 创建并打开一个窗体，设置窗体的大小，最简单的代码仅需3行。

    from Tkinter import *
    root = Tk()		#创建窗口对象
    root.mainloop()		#运行窗口对象

除此之外，针对窗口有许多丰富的操作，详细可以在官网上查询，这里只列出我实际应用过程中用到的。如：

设置窗口大小
---
    root.maxsize(80*8,650)
    root.minsize(80*8,650)

设置固定窗口大小
---

	root.resizable(width=False, height=False)

自定义关闭按钮（即窗口页面的‘×’）
---
	
	# 其中destory_window 为自定义的对应的调用函数，
	root.protocol('WM_DELETE_WINDOW', destory_window) 

	# 如果需要传入参数，则用lambda的方式
	root.protocol('WM_DELETE_WINDOW', lambda: destory_window(arg1,arg2)) 

窗口设为置顶
---

	root.wm_attributes('-topmost',1)

插入label控件
---

	label_top = Label(root, text=u"标签名称", font=('Arial', 25))
	label_top.grid(row=0, column=1, columnspan=1)

使用grid对页面布局
---

	button1 = Button(self.root, text='按钮1', command = func1)
    button2 = Button(self.root, text='按钮2', command = func2)
    button3 = Button(self.root, text='按钮3', command = func3)
    button4 = Button(self.root, text='按钮4', command = func4)
    button1.grid(row=0,column=0)
    button2.grid(row=0,column=2)
    button3.grid(row=1,column=1)
    button4.grid(row=1,column=3)

登录界面
---
  这里以登录窗口为例，包括“用户名”， “密码”， “确认”按钮。
	
	# -*- coding:utf-8 -*-
	from Tkinter import *
	
	def check_login(uname,passwd):
	    print uname
	    print passwd
	    
	root = Tk()
	var_user = StringVar() 
	var_user.set("用户名默认值")
	label_user = Label(root, text=u'用户名')
	entry_user = Entry(root, textvariable=var_user)
	label_user.grid(row=4,column=0)
	entry_user.grid(row=4,column=1, columnspan=2)
	
	var_passwd = StringVar()
	var_passwd.set("密码默认值")
	label_passwd = Label(root, text=u'密码')
	entry_passwd = Entry(root, textvariable=var_passwd, show="*")
	label_passwd.grid(row=5,column=0)
	entry_passwd.grid(row=5,column=1, columnspan=2)
	
	btn_submit = Button(root, text="登录", command = lambda: check_login(var_user.get(),var_passwd.get()))
	btn_close = Button(root, text="取消", command = root.destroy)
	btn_submit.grid(row=6, column=0)
	btn_close.grid(row=6, column=2)
	root.mainloop()

*这里需要特别注意的有，如果登录窗口是从另一个窗口触发，且需要回到上一级窗口去处理对于的参数时，要将登录窗口由 Tk() 改为 Toplevel()，否则页面修改的参数没法自动刷新。简单的说，如果发现默认值设置没生效，而且确定后没有使用在文本输入的值，就试下把 Tk() 改成 Toplevel() 吧。*

设置文本框只读
---
  除了上面登录中使用的设置文本框默认值的方法，还有一种方法也可以设置默认值。

	note_entry = Entry(root)
	note_entry.insert(END, "默认值")
	note_entry['state'] = 'readonly'

创建菜单
---

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

弹出信息窗口
---

    import tkMessageBox
    def alert(self, title="Info", msg=""):
        msb = tkMessageBox.showinfo(title, msg)

弹出确认窗口
---
  askyesno窗口会有“是”，“否”的选项，根据用户选择返回True/False

    def yesno(self, title="Info", msg=""):
        return tkMessageBox.askyesno(title, msg) 