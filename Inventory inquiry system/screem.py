import tkinter as tk
from tkinter import END, ttk, messagebox, Tk, filedialog
from order_def import Order_def
import os
# 获取桌面路径
desktop_path = os.path.expanduser('~/桌面')
# 设置导出Excel时首次打开时显示的目录
excel_save_path = desktop_path 

# 当点击按钮时触发,调用按钮对应的画布
def show_page(page_name, clicked_button):
    # 所有按钮主题还原
    for button in button_widgets:
        button.configure(**button_style)
    # 改变选中的主题
    clicked_button.configure(**pitch_button_style)
    # 清空画布
    global canvas
    canvas.destroy()
    canvas = tk.Canvas(window, width=canvas_width, height=canvas_height)
    canvas.grid(row=0, column=2)

    # 判断调用哪个画布
    if page_name == "采购订单添加":
        add_PO_page()
    elif page_name == "采购订单查询":
        show_PO_page()
    elif page_name == "销售订单添加":
        add_GO_page()
    elif page_name == "销售订单查询":
        show_GO_page()
    elif page_name == "库存查询":
        inventory_query_page()
    elif page_name == "信息修改":
        update_sale_price_page()
    elif page_name == "备份":
        copy_page()
    elif page_name == "SQL输入":
        how_update_input_SQL_page()

#================下方为各个页面内容函数========================================
# 添加采购订单
def add_PO_page():
    
    global canvas
    global var_supplier
    global var_goods_gname
    #初始化下拉框的值
    var_supplier = tk.StringVar()
    var_goods_gname = tk.StringVar()

    # 创建标题
    title_label = tk.Label(canvas, text="采购订单添加", font=("Arial", 20))
    title_label.place(x=canvas_width/2, y=50, anchor="center")

    # 创建标签和输入框
    label1 = tk.Label(canvas, text="供货商名称:", font=("Arial", 12))
    label1.place(x=150, y=150)

    label2 = tk.Label(canvas, text="名称型号:", font=("Arial", 12))
    label2.place(x=150, y=200)

    label4 = tk.Label(canvas, text="采购时间:", font=("Arial", 12))
    label4.place(x=150, y=250)
    entry4 = tk.Entry(canvas, font=("Arial", 12), width=30)
    entry4.place(x=250, y=260, anchor="w")

    label3 = tk.Label(canvas, text="采购数量:", font=("Arial", 12))
    label3.place(x=150, y=300)
    entry3 = tk.Entry(canvas, font=("Arial", 12), width=30)
    entry3.place(x=250, y=310, anchor="w")

    label5 = tk.Label(canvas, text="采购成本:", font=("Arial", 12))
    label5.place(x=150, y=350)
    entry5 = tk.Entry(canvas, font=("Arial", 12), width=30)
    entry5.place(x=250, y=360, anchor="w")

    # 获取供货商名称的提示词列表
    def re_supplier_callword(*args):
        #把get_supplier_callword返回值作为下拉框列表
        supplier_callwords_combobox['values'] = od.get_supplier_callword(
            supplier_callwords_combobox.get())
    # 初始化下拉框提示词列表(全部)
    supplier_callwords = od.get_supplier_callword()
    supplier_callwords_combobox = ttk.Combobox(
        canvas, textvariable=var_supplier, values=supplier_callwords, font=("Arial", 12), width=28)
    #下拉框位置
    supplier_callwords_combobox.place(x=250, y=160, anchor="w")
    #监听内容变化
    var_supplier.trace("w", re_supplier_callword)

    # 获取名称型号的提示词列表
    def re_goods_callword(*args):
        #返回值作为下拉框列表
        goods_callwords_combobox['values'] = od.get_goods_gname_callword(
            goods_callwords_combobox.get())
    #初始化提示列表内容
    goods_callwords = od.get_goods_gname_callword()
    goods_callwords_combobox = ttk.Combobox(
        canvas, textvariable=var_goods_gname, values=goods_callwords, font=("Arial", 12), width=28)
    goods_callwords_combobox.place(x=250, y=210, anchor="w")
    #监听内容变化
    var_goods_gname.trace("w", re_goods_callword)

    # 创建确定按钮
    def add_PO_handler():
        #读取各个框中的内容->准备参数
        supplier_name = supplier_callwords_combobox.get()
        goods_name = goods_callwords_combobox.get()
        quantity = entry3.get()
        purchase_time = entry4.get()
        cost = entry5.get()
        #如果没有成功调用add_PO根据错误进行修改后再次调用
        while True:
            # 调用添加采购订单函数并获取返回值
            is_true = od.add_PO(supplier_name, goods_name,
                                quantity, purchase_time, cost)
            # 成功调用
            if is_true == 1:
                #清空各个框的内容
                supplier_callwords_combobox.delete(0, END)
                goods_callwords_combobox.delete(0, END)
                entry3.delete(0, END)
                entry4.delete(0, END)
                entry5.delete(0, END)
                break
            #如果因为没有商品信息报错
            elif is_true == 2:
                confirm = messagebox.askquestion("确认操作", "数据库中没有该商品信息，是否继续？")
                #确认后自动添加商品信息
                if confirm == 'yes':
                    od.add_goods(goods_name) 
                else:
                    break
            #如果因为没有供货商信息报错
            elif is_true == 3:
                confirm = messagebox.askquestion("确认操作", "数据库中没有该供货商信息，是否继续？")
                #确认后自动添加
                if confirm == 'yes':
                    od.add_supplier(supplier_name)  
                else:
                    break
            else:
                messagebox.showerror("输入有误", "请输入正确的采购订单信息")
                break
    #确定按钮,点击确定后尝试提交采购订单
    button = tk.Button(canvas, text="确定", bg="#4a90e2", fg="white", font=("Arial", 12),
                       width=10, height=2, bd=0, relief="ridge",
                       command=add_PO_handler)
    button.place(x=250, y=450, anchor="center")

# 查询采购订单
def show_PO_page():
    
    global canvas
    global var_supplier
    global var_goods_gname
    #初始化下拉框的值
    var_supplier = tk.StringVar()
    var_goods_gname = tk.StringVar()
    #名称和输入框
    product_label = tk.Label(canvas, text="名称型号:", font=("Arial", 12))
    product_label.place(x=50, y=60)

    supplier_label = tk.Label(canvas, text="供货商名:", font=("Arial", 12))
    supplier_label.place(x=290, y=60)

    b_time = tk.Label(canvas, text="起始时间:", font=("Arial", 12))
    b_time.place(x=530, y=60)
    b_time_entry = tk.Entry(canvas, font=("Arial", 12), width=17)
    b_time_entry.place(x=605, y=73, anchor="w")

    e_time = tk.Label(canvas, text="结束时间:", font=("Arial", 12))
    e_time.place(x=770, y=60)
    e_time_entry = tk.Entry(canvas, font=("Arial", 12), width=17)
    e_time_entry.place(x=845, y=73, anchor="w")
    
    # 获取商品名称的提示词列表
    def re_goods_callword(*args):
        #根据返回值确定下拉框列表的值
        goods_callwords_combobox['values'] = od.get_goods_gname_callword(
            goods_callwords_combobox.get())
    #初始化提示词列表
    goods_callwords = od.get_goods_gname_callword()
    goods_callwords_combobox = ttk.Combobox(
        canvas, textvariable=var_goods_gname, values=goods_callwords, font=("Arial", 12), width=15)
    #放置下拉框
    goods_callwords_combobox.place(x=125, y=73, anchor="w")
    #监听文本变化
    var_goods_gname.trace("w", re_goods_callword)
    
    #获取供应商的提示词列表
    def re_supplier_callword(*args):
        #根据返回值确定下拉框列表的值
        supplier_callwords_combobox['values'] = od.get_supplier_callword(
            supplier_callwords_combobox.get())
    #初始化提示词列表
    supplier_callwords = od.get_supplier_callword()
    supplier_callwords_combobox = ttk.Combobox(
        canvas, textvariable=var_supplier, values=supplier_callwords, font=("Arial", 12), width=15)
    supplier_callwords_combobox.place(x=365, y=73, anchor="w")
    #监听文本变化
    var_supplier.trace("w", re_supplier_callword)
    #初始化数据(因为列表的地址不会变,如果直接=None,获取到的数据只会存在内部函数作用域)
    data = [None]
    #根据数据可视化为表格
    def query_inventory():
        #获取各个框内的值作为参数
        product = goods_callwords_combobox.get()
        supplier = supplier_callwords_combobox.get()
        b__time = b_time_entry.get()
        e__time = e_time_entry.get()
        #获取数据
        data[0] = od.found_PO(product, supplier, b__time, e__time)
        # 创建表头
        table = ttk.Treeview(canvas, columns=(
            'cname', 'gname', 'p_price', 'qty_num', 'qty_weight', 'p_date'))
        #设置位置
        table.place(x=30, y=140, height=550)
        #设置名称
        table.heading("cname", text="供货商名称")
        table.heading("gname", text="名称型号")
        table.heading("p_price", text="售价")
        table.heading("qty_num", text="数量(件)")
        table.heading("qty_weight", text="数量(kg)")
        table.heading("p_date", text="日期")
        #设置宽度
        table.column("cname", width=170)
        table.column("gname", width=170)
        table.column("p_price", width=165)
        table.column("qty_num", width=165)
        table.column("qty_weight", width=165)
        table.column("p_date", width=165)
        # 添加数据
        for row in data[0]:
            table.insert(parent='', index='end', values=row)
    #确定按钮,根据检索条件读取出数据
    button = tk.Button(canvas, text="确定",
                       command=query_inventory, **button_style)
    button.place(x=1150, y=70, anchor="center")
    #初始化表格
    query_inventory()
    # 导出表格数据
    def export_data():
        root = Tk()
        root.withdraw()  # 隐藏根窗口

        # 打开文件选择对话框，找到存储位置
        export_path = filedialog.asksaveasfilename(initialdir=excel_save_path, defaultextension=".xlsx", title="采购订单导出路径",
                                                   filetypes=(('EXCEL文件', '*.xlsx'), ("All files", "*.*")))
        root.destroy()  # 销毁根窗口
        #如果用户点保存则得到路径
        if export_path:
            # 调用od.make_excel函数，传递导出路径参数
            export_result = od.make_excel(
                data[0], export_path, ['供货商名称', '商品名称', '售价', '数量(件)', '数量(kg)', '日期'])

            if export_result:
                messagebox.showinfo("提示", "导出成功")
            else:
                messagebox.showinfo("警告", "导出失败")

    # 导出按钮
    export_button = tk.Button(
        canvas, text="导出", command=export_data, **button_style)
    export_button.place(x=580, y=720, anchor="center")

# 添加销售订单
def add_GO_page():
    
    global canvas
    global var_goods_gname
    global var_customer
    #初始化下拉框内容
    var_customer = tk.StringVar()
    var_goods_gname = tk.StringVar()

    # 创建标题
    title_label = tk.Label(canvas, text="销售订单添加", font=("Arial", 20))
    title_label.place(x=canvas_width/2, y=50, anchor="center")

    # 创建标签和输入框
    c_label = tk.Label(canvas, text="客户名称:", font=("Arial", 12))
    c_label.place(x=150, y=150)

    goods_label = tk.Label(canvas, text="名称型号:", font=("Arial", 12))
    goods_label.place(x=150, y=200)

    qty_label = tk.Label(canvas, text="订购时间:", font=("Arial", 12))
    qty_label.place(x=150, y=250)
    date_entry = tk.Entry(canvas, font=("Arial", 12), width=30)
    date_entry.place(x=250, y=260, anchor="w")

    qty_label = tk.Label(canvas, text="订购数量:", font=("Arial", 12))
    qty_label.place(x=150, y=300)
    qty_entry = tk.Entry(canvas, font=("Arial", 12), width=30)
    qty_entry.place(x=250, y=310, anchor="w")

    price_label = tk.Label(canvas, text="订购价格:", font=("Arial", 12))
    price_label.place(x=150, y=350)
    price_entry = tk.Entry(canvas, font=("Arial", 12), width=30)
    price_entry.place(x=250, y=360, anchor="w")

    # 获取商品名称的提示词列表
    def re_goods_callword(*args):
        #根据返回值确定下拉框列表的值
        goods_callwords_combobox['values'] = od.get_goods_gname_callword(
            goods_callwords_combobox.get())
    #初始化下拉框列表
    goods_callwords = od.get_goods_gname_callword()
    #创建下拉框
    goods_callwords_combobox = ttk.Combobox(
        canvas, textvariable=var_goods_gname, values=goods_callwords, font=("Arial", 12), width=28)
    goods_callwords_combobox.place(x=250, y=210, anchor="w")
    #监听文字变化
    var_goods_gname.trace("w", re_goods_callword)
    
    # 获取客户的提示词列表
    def re_customer_callword(*args):
        #根据返回值确定下拉框列表的值
        customer_callwords_combobox['values'] = od.get_customer_callword(
            customer_callwords_combobox.get())
    #初始化下拉框列表
    customer_callwords = od.get_customer_callword()
    #创建下拉框
    customer_callwords_combobox = ttk.Combobox(
        canvas, textvariable=var_customer, values=customer_callwords, font=("Arial", 12), width=28)
    customer_callwords_combobox.place(x=250, y=160, anchor="w")
    #监听文字变化
    var_customer.trace("w", re_customer_callword)

    # 创建确定按钮
    def add_GO_handler():
        #获取输入框内容->准备参数
        gname = goods_callwords_combobox.get()
        cname = customer_callwords_combobox.get()
        qty = qty_entry.get()
        data = date_entry.get()
        price = price_entry.get()
        #执行添加销售订单,并获取是否成功
        is_true = od.add_GO(gname, cname, qty, data, price)
        if is_true:
            #清除框内内容
            customer_callwords_callwords_combobox.delete(0, END)
            goods_callwords_combobox.delete(0, END)
            qty_entry.delete(0, END)
            date_entry.delete(0, END)
            price_entry.delete(0, END)
        else:
            messagebox.showerror("输入有误", "请输入正确的采购订单信息")
    #确定按钮
    button = tk.Button(canvas, text="确定", bg="#4a90e2", fg="white", font=("Arial", 12),
                       width=10, height=2, bd=0, relief="ridge",
                       command=add_GO_handler)
    button.place(x=250, y=450, anchor="center")

# 查询销售订单
def show_GO_page():

    global canvas
    global var_customer
    global var_goods_type
    #初始化下拉框内容
    var_customer = tk.StringVar()
    var_goods_gname = tk.StringVar()
    # 创建标签和输入框  
    product_label = tk.Label(canvas, text="名称型号:", font=("Arial", 12))
    product_label.place(x=50, y=60)

    customer_label = tk.Label(canvas, text="客户名:", font=("Arial", 12))
    customer_label.place(x=290, y=60)

    b_time = tk.Label(canvas, text="起始时间:", font=("Arial", 12))
    b_time.place(x=530, y=60)
    b_time_entry = tk.Entry(canvas, font=("Arial", 12), width=17)
    b_time_entry.place(x=605, y=73, anchor="w")

    e_time = tk.Label(canvas, text="结束时间:", font=("Arial", 12))
    e_time.place(x=770, y=60)
    e_time_entry = tk.Entry(canvas, font=("Arial", 12), width=17)
    e_time_entry.place(x=845, y=73, anchor="w")
    
    # 获取商品名称的提示词列表
    def re_goods_callword(*args):
        #根据返回值确定下拉框列表内容
        goods_callwords_combobox['values'] = od.get_goods_gname_callword(
            goods_callwords_combobox.get())
    #初始化下拉框列表内容
    goods_callwords = od.get_goods_gname_callword()
    #创建下拉框
    goods_callwords_combobox = ttk.Combobox(
        canvas, textvariable=var_goods_gname, values=goods_callwords, font=("Arial", 12), width=15)
    goods_callwords_combobox.place(x=125, y=73, anchor="w")
    #监听文字变化
    var_goods_gname.trace("w", re_goods_callword)
    # 获取客户的提示词列表
    def re_customer_callword(*args):
        #根据返回值确定下拉框列表内容
        customer_callwords_combobox['values'] = od.get_customer_callword(
            customer_callwords_combobox.get())
    #初始化下拉框列表内容
    customer_callwords = od.get_customer_callword()
    #创建下拉框
    customer_callwords_combobox = ttk.Combobox(
        canvas, textvariable=var_customer, values=customer_callwords, font=("Arial", 12), width=15)
    customer_callwords_combobox.place(x=365, y=73, anchor="w")
    #监听文字变化
    var_customer.trace("w", re_customer_callword)
    #初始化数据(因为列表的地址不会变,如果直接=None,获取到的数据只会存在内部函数作用域)
    data = [None]
    #根据数据可视化为表格
    def query_inventory():
        #获取输入框内容作为参数
        product = goods_callwords_combobox.get()
        customer = customer_callwords_combobox.get()
        b__time = b_time_entry.get()
        e__time = e_time_entry.get()
        #获取数据
        data[0] = od.found_GO(product, customer, b__time, e__time)
        # 创建表头
        table = ttk.Treeview(canvas, columns=(
            'sname', 'gtype', 'g_price', 'inv_price', 'qty_num', 'qty_weight', 'p_date', 'profit'))
        #设置位置
        table.place(x=30, y=140, height=550)
        #设置列名
        table.heading("sname", text="客户名称")
        table.heading("gtype", text="商品名称")
        table.heading("g_price", text="售价")
        table.heading("inv_price", text="成本")
        table.heading("qty_num", text="数量(件)")
        table.heading("qty_weight", text="数量(kg)")
        table.heading("p_date", text="日期")
        table.heading("profit", text="利润")
        #设置列宽
        table.column("sname", width=135)
        table.column("gtype", width=135)
        table.column("g_price", width=120)
        table.column("inv_price", width=120)
        table.column("qty_num", width=120)
        table.column("qty_weight", width=120)
        table.column("p_date", width=130)
        table.column("profit", width=120)

        # 添加数据
        for row in data[0]:
            table.insert(parent='', index='end', values=row)
    #根据筛选条件筛出需要信息
    button = tk.Button(canvas, text="确定",
                       command=query_inventory, **button_style)
    button.place(x=1150, y=70, anchor="center")
    query_inventory()
    #导出操作
    def export_data():
        root = Tk()
        root.withdraw()  # 隐藏根窗口

        # 打开文件选择对话框，选择保存路径
        export_path = filedialog.asksaveasfilename(initialdir=excel_save_path, defaultextension=".xlsx", title="销售订单导出路径",
                                                   filetypes=(('EXCEL文件', '*.xlsx'), ("All files", "*.*")))
        root.destroy()  # 销毁根窗口
        # 如果点击保存则导出
        if export_path:
            export_result = od.make_excel(
                data[0], export_path, ['客户名称', '商品名称', '售价', '成本',  '数量(件)', '数量(kg)', '日期', '利润'])

            if export_result:
                messagebox.showinfo("提示", "导出成功")
            else:
                messagebox.showinfo("警告", "导出失败")

    # 添加底部输入框和导出按钮

    export_button = tk.Button(
        canvas, text="导出", command=export_data, **button_style)
    export_button.place(x=580, y=720, anchor="center")

#查询库存
def inventory_query_page():

    global canvas
    global var_customer
    global var_goods_type
    #初始化下拉框内容
    var_customer = tk.StringVar()
    var_goods_type = tk.StringVar()
    #提示词和输入框
    product_label = tk.Label(canvas, text="商品名称:", font=("Arial", 12))
    product_label.place(x=50, y=60)

    ply_label = tk.Label(canvas, text="商品厚度:", font=("Arial", 12))
    ply_label.place(x=390, y=60)
    ply_entry = tk.Entry(canvas, font=("Arial", 12), width=25)
    ply_entry.place(x=480, y=70, anchor="w")

    width_label = tk.Label(canvas, text="商品宽度:", font=("Arial", 12))
    width_label.place(x=730, y=60)
    width_entry = tk.Entry(canvas, font=("Arial", 12), width=25)
    width_entry.place(x=820, y=70, anchor="w")
    
    
    # 获取商品类型提示词列表
    def re_goods_type_callword(*args):
        #根据返回的数据作为下拉框提示词
        goods_type_callwords_combobox['values'] = od.get_goods_type_callword(
            goods_type_callwords_combobox.get())
    #初始化下拉框提示词
    goods_type_callwords = od.get_goods_type_callword()
    #创建下拉框
    goods_type_callwords_combobox = ttk.Combobox(
        canvas, textvariable=var_goods_type, values=goods_type_callwords, font=("Arial", 12), width=23)
    goods_type_callwords_combobox.place(x=140, y=70, anchor="w")
    #监听文本变化
    var_goods_type.trace("w", re_goods_type_callword)
    #初始化数据(因为列表的地址不会变,如果直接=None,获取到的数据只会存在内部函数作用域)
    data = [None]
    #根据数据可视化为表格
    def query_inventory():
        #获取框内数据作为参数
        gtype = goods_type_callwords_combobox.get()
        ply = ply_entry.get()
        width = width_entry.get()
        #获取表格数据
        data[0] = od.found_goods(gtype, ply, width)

        # 创建表头
        table = ttk.Treeview(canvas, columns=(
            "gname", "ply", "width", "cost", "qty_num", 'qty_weight'))
        #设置位置
        table.place(x=30, y=140, height=550)
        #设置列名
        table.heading("gname", text="商品型号")
        table.heading("ply", text="厚度")
        table.heading("width", text="宽度")
        table.heading("cost", text="平均成本")
        table.heading("qty_num", text="数量(件)")
        table.heading("qty_weight", text="数量(kg)")
        #设置列宽
        table.column("gname", width=175)
        table.column("ply", width=165)
        table.column("width", width=165)
        table.column("cost", width=165)
        table.column("qty_num", width=165)
        table.column("qty_weight", width=165)
        # # 添加数据
        for row in data[0]:
            table.insert(parent='', index='end', values=row)
    #确定按钮
    button = tk.Button(canvas, text="确定",
                       command=query_inventory, **button_style)
    button.place(x=1150, y=70, anchor="center")
    query_inventory()
    #导出
    def export_data():
        root = Tk()
        root.withdraw()  # 隐藏根窗口

        # 打开文件选择对话框，获取文件路径
        export_path = filedialog.asksaveasfilename(initialdir=excel_save_path, defaultextension=".xlsx", title="库存数据导出路径",
                                                   filetypes=(('EXCEL文件', '*.xlsx'), ("All files", "*.*")))
        root.destroy()  # 销毁根窗口
        # 如果点保存根据路径保存数据
        if export_path:
            export_result = od.make_excel(
                data[0], export_path, ['商品名称', '厚度', '宽度', '平均成本', '数量(件)', '数量(kg)'])

            if export_result:
                messagebox.showinfo("提示", "导出成功")
            else:
                messagebox.showinfo("警告", "导出失败")

    # 添加底部输入框和导出按钮

    export_button = tk.Button(
        canvas, text="导出", command=export_data, **button_style)
    export_button.place(x=580, y=720, anchor="center")

#信息修改界面:添加供货商,添加客户,添加商品信息
def update_sale_price_page():
    
    global canvas
    global var_goods_gname
    global var_customer
    #初始化列表内容
    var_customer = tk.StringVar()
    var_goods_gname = tk.StringVar()
    
    #卖给客户商品价格修改与添加
    #提示词和输入框
    title_label = tk.Label(canvas, text="信息修改", font=("Arial", 20))
    title_label.place(x=canvas_width/2, y=50, anchor="center")

    purchase_label = tk.Label(canvas, text="客户名称:", font=("Arial", 12))
    purchase_label.place(x=150, y=150)

    product_label = tk.Label(canvas, text="商品名称:", font=("Arial", 12))
    product_label.place(x=150, y=200)

    price_label = tk.Label(canvas, text="售价:", font=("Arial", 12))
    price_label.place(x=150, y=250)
    price_entry = tk.Entry(canvas, font=("Arial", 12), width=30)
    price_entry.place(x=250, y=260, anchor="w")

    # 获取商品名称的提示词列表
    def re_goods_callword(*args):
        #根据返回值确定提示词列表
        goods_callwords_combobox['values'] = od.get_goods_gname_callword(
            goods_callwords_combobox.get())
    #初始化提示此列表
    goods_callwords = od.get_goods_gname_callword()
    #创建下拉框
    goods_callwords_combobox = ttk.Combobox(
        canvas, textvariable=var_goods_gname, values=goods_callwords, font=("Arial", 12), width=28)
    goods_callwords_combobox.place(x=250, y=210, anchor="w")
    #监听文字变化
    var_goods_gname.trace("w", re_goods_callword)
    
    #获取客户的提示词列表
    def re_customer_callword(*args):
        #根据返回值确定提示词列表
        customer_callwords_combobox['values'] = od.get_customer_callword(
            customer_callwords_combobox.get())
    #初始化提示此列表
    customer_callwords = od.get_customer_callword()
    #创建下拉框
    customer_callwords_combobox = ttk.Combobox(
        canvas, textvariable=var_customer, values=customer_callwords, font=("Arial", 12), width=28)
    customer_callwords_combobox.place(x=250, y=160, anchor="w")
    #监听文字变化
    var_customer.trace("w", re_customer_callword)
    # 创建确定按钮

    def update_sale_price():
        #根据输入框内容作为参数
        purchase = customer_callwords_combobox.get()
        product = goods_callwords_combobox.get()
        price = price_entry.get()
        #执行修改卖给客户的价格并获取是否成功
        is_true=od.update_price(purchase, product, price)
        if  is_true:
            #清空输入框内容
            customer_callwords_combobox.delete(0, END)
            goods_callwords_combobox.delete(0, END)
            price_entry.delete(0, END)
        else:
            messagebox.showinfo("提示", "输入有误，请输入正确的采购订单信息")
    #确定按钮
    button = tk.Button(canvas, text="确定",
                       command=update_sale_price, **button_style)
    button.place(x=350, y=310, anchor="center")


    #添加供货商
    #提示词和输入框
    supplier_label = tk.Label(canvas, text="供货商名称:", font=("Arial", 12))
    supplier_label.place(x=700, y=150)
    supplier_entry = tk.Entry(canvas, font=("Arial", 12), width=30)
    supplier_entry.place(x=800, y=160, anchor="w")
    
    #添加供货商
    def add_supplier():
        #获取参数
        sname=supplier_entry.get()
        #增加供货商并获取是否成功
        is_true=od.add_supplier(sname)
        if is_true:
            # 清空输入框
            supplier_entry.delete(0, END)  
        else:
            messagebox.showinfo("提示", "输入有误，请输入正确的采购订单信息")

    button = tk.Button(canvas, text="添加", command=add_supplier, **button_style)
    button.place(x=900, y=210, anchor="center")
    
    
    #商品信息添加
    #提示词和输入框
    product2_label = tk.Label(canvas, text="名称型号:", font=("Arial", 12))
    product2_label.place(x=700, y=250)
    product2_entry = tk.Entry(canvas, font=("Arial", 12), width=30)
    product2_entry.place(x=800, y=260, anchor="w")

    #添加商品信息
    def update_product2_info():
        product = product2_entry.get()
        is_true=od.add_goods(product)
        if is_true:
            # 清空输入框
            product2_entry.delete(0, END) 
        else:
            messagebox.showinfo("提示", "输入有误，请输入正确的格式")

    button = tk.Button(canvas, text="添加",
                       command=update_product2_info, **button_style)
    button.place(x=900, y=310, anchor="center")

#手动备份,导入备份数据,执行操作记录
def copy_page():

    global canvas
    
    #手动备份
    def copy_database():
        root = Tk()
        root.withdraw()  # 隐藏根窗口
        # 打开文件选择对话框，选择保存路径
        file_path = filedialog.asksaveasfilename(initialdir='手动备份', defaultextension=".sql", title="库存数据导出路径",
                                                 filetypes=(('SQL文件', '*.sql'),))
        root.destroy()  # 销毁根窗口
        #如果点保存则进行当前数据库备份
        if file_path:
            # 调用备份方法并获取是否备份成功
            is_true = od.copy_database(file_path)

            if is_true:
                messagebox.showinfo("提示", "导出成功")
            else:
                messagebox.showinfo("提示", "输入有误，请输入正确的路径")
    # 创建输入框和确定按钮
    copy_button = tk.Button(canvas, text="手动备份",
                            command=copy_database, **button_style)
    copy_button.place(x=canvas_width/2, y=200, anchor="center")

    #执行备份文件
    def recover_database():
        root = Tk()
        root.withdraw()  # 隐藏根窗口
        # 打开文件选择对话框，允许选择单个文件
        file_path = filedialog.askopenfilename(
            initialdir="数据备份", title="读取备份文件", filetypes=(("sql files", "*.sql"),))
        root.destroy()  # 销毁根窗口
        if file_path:
            # 运行sql语句
            is_true = od.run_SQL_file(file_path)

            if is_true:
                messagebox.showinfo("提示", "导出入成功")
            else:
                messagebox.showinfo("提示", "输入有误，请输入正确的路径")

    copy_button = tk.Button(canvas, text="读取备份",
                            command=recover_database, **button_style)
    copy_button.place(x=canvas_width/2, y=400, anchor="center")

    #执行操作记录
    def rework_handle():
        root = Tk()
        root.withdraw()  # 隐藏根窗口
        # 打开文件选择对话框，允许选择单个文件
        file_path = filedialog.askopenfilename(
            initialdir="操作记录", title="运行操作记录", filetypes=(("txt files", "*.txt"),))
        root.destroy()  # 销毁根窗口
        if file_path.strip():
            # 调用操作方法
            print(f"od.run_txt_file({file_path})")
            is_ture = od.run_txt_file(file_path)

            if is_ture:
                messagebox.showinfo("提示", "导出成功")
            else:
                messagebox.showinfo("提示", "输入有误，请输入正确的路径")

    copy_button = tk.Button(canvas, text="运行操作记录",
                            command=rework_handle, **button_style)
    copy_button.place(x=canvas_width/2, y=600, anchor="center")

# SQL
def how_update_input_SQL_page():

    global canvas
    # 创建输入框和确定按钮
    input_label = tk.Label(canvas, text="请输入SQL语句:", font=("Arial", 12))
    input_label.place(x=canvas_width/2, y=80, anchor="center")

    input_entry = tk.Entry(canvas, font=("Arial", 12), width=50)
    input_entry.place(x=canvas_width/2, y=180, anchor="center")
    #执行sql语句
    def run_SQL():
        sql = input_entry.get()
        if od.run_SQL_code(sql):
            input_entry.delete(0, END)  # 清空输入框
        else:
            messagebox.showinfo("提示", "输入有误，请输入正确的sql")
    button = tk.Button(canvas, text="确定", command=run_SQL, **button_style)
    button.place(x=canvas_width/2, y=300, anchor="center")

#创建连接数据库对象
od = Order_def('配置文件\数据库账号和密码.JSON')
# 创建主窗口
window = tk.Tk()
var_supplier = tk.StringVar()
var_goods_gname = tk.StringVar()
var_goods_type = tk.StringVar()
var_customer = tk.StringVar()

# 获取屏幕大小
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# 设置窗口大小
window.geometry(f"{screen_width}x{screen_height}")

# 创建左侧按钮
button_frame = tk.Frame(window, bg="#f0f0f0")
button_frame.grid(row=0, column=0, sticky="ns")

# 设置按钮样式
#未选中的格式
button_style = {"bg": "#4a90e2", "fg": "white", "font": (
    "Arial", 12), "width": 20, "height": 2, "bd": 0, "relief": "ridge"}
#选中的格式
pitch_button_style = {
    "bg": "#FF6347",  # Background color
    "fg": "#FFFFFF",  # Foreground color (text color)
    "font": ("Helvetica", 14, "bold"),  # Font style
    "width": 15,  # Width of the button
    "height": 2,  # Height of the button
    "bd": 0,  # Border width
    "relief": "groove",  # Border style
    # Background color when the button is under the cursor
    "activebackground": "#FF4500",
    "activeforeground": "#FFFFFF"  # Foreground color when the button is under the cursor
}
# 创建按钮
buttons = ["采购订单添加", "采购订单查询", "销售订单添加", "销售订单查询",
           "库存查询", "备份", "信息修改", "SQL输入"]
button_widgets = []  # Store all button widgets
for i, button_text in enumerate(buttons):
    button = tk.Button(button_frame, text=button_text, **button_style)
    button.grid(row=i, column=0, padx=10, pady=10)
    button.configure(command=lambda page=button_text,
                     btn=button: show_page(page, btn))
    button_widgets.append(button)  # Add the button widget to the list

# 创建画布覆盖右侧空白部分
canvas_width = screen_width * 0.8
canvas_height = screen_height
canvas = tk.Canvas(window, width=canvas_width, height=canvas_height)
canvas.grid(row=0, column=1)

# 设置画布背景颜色
canvas.configure(bg="white")

# 运行窗口
window.mainloop()
