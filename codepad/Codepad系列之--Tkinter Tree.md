Codepad系列之--Tkinter Tree
===

创建Tree
---

	# -*- coding:utf-8 -*-
	from Tkinter import *
	import ttk
	
	root = Tk()
	tree=ttk.Treeview(root, show="headings")      #初始化表格  
	tree["columns"]=("姓名","性别","年龄","电话")   #设置表头
	
	# 设置每一列的宽度
	tree.column("姓名",width=80)
	tree.column("性别",width=80) 
	tree.column("年龄",width=40) 
	tree.column("电话",width=160)
	
	for t_name in tree["columns"]:
	    #显示表头信息，表头信息通过text参数指定
	    tree.heading(t_name,text=t_name)
	
	# 设置每一行数据
	data_list = []
	data_list.append( ("赵一", "男" , "11", "110") )
	data_list.append( ("钱二", "女" , "12", "101") )
	data_list.append( ("孙三", "男" , "13", "011") )
	data_list.append( ("李四", "女" , "14", "001") )
	
	# 在表格中插入数据
	for temp in data_list:
	    tree.insert("",0,values=temp)
	    
	# 显示表格
	tree.grid(row=0, column=0)
	root.mainloop()

获取当前选中行
---

	selected_items = tree.selection() 
    if not bool(selected_items):
        print "no item selected"
    for one_item in selected_items:
        print tree.item(one_item)['values']

  其中 selected_items 是一个列表，列表内每个元素就是选择的一行，也就是说如果选择多行，也是可以一起处理的。

刷新列表
--

	# 删除原来的数据
	tree.delete(*self.tree.get_children())

	# 重新设置每一行数据
	data_list = []
	data_list.append( ("赵一", "男" , "21", "310") )
	data_list.append( ("钱二", "女" , "22", "301") )
	data_list.append( ("孙三", "男" , "23", "311") )
	data_list.append( ("李四", "女" , "24", "301") )

	# 在表格中插入数据
	for temp in data_list:
	    tree.insert("",0,values=temp)
	    
