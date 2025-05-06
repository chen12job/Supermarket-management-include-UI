from basic import Basic
from commodity import Commodity
from prettytable import PrettyTable
from purchaser import Purchaser
import os
import generaloperat
from purchaser import Purchaser
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import simpledialog


class PurchaseManage:

    def __init__(self):
        self.admin = None
        self.window = None

    def show_gui(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("进货员界面")
        self.window.geometry("800x600")

        # 设置窗口背景色
        self.window.configure(bg='#f0f0f0')

        # 配置窗口网格权重
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)

        # 创建主容器
        main_container = tk.Frame(self.window, bg='#f0f0f0')
        main_container.grid(row=0, column=0, sticky="nsew")
        main_container.grid_rowconfigure(0, weight=1)
        main_container.grid_columnconfigure(0, weight=1)

        if not self.login_gui():
            self.window.destroy()
            return

        self.create_main_menu()

    def login_gui(self):
        login_window = tk.Toplevel(self.window)
        login_window.title("登录")
        login_window.geometry("300x200")
        login_window.configure(bg='#f0f0f0')

        # 配置登录窗口网格权重
        login_window.grid_rowconfigure(0, weight=1)
        login_window.grid_columnconfigure(0, weight=1)

        # 创建主框架
        main_frame = ttk.Frame(login_window, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")

        # 创建输入框架
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(expand=True, fill="both", pady=20)

        ttk.Label(input_frame, text="编号:").pack(pady=5)
        username_entry = ttk.Entry(input_frame, width=20)
        username_entry.pack(pady=5)

        login_success = [False]

        def try_login():
            pur_num = username_entry.get().strip()
            pur = Basic.queryOnePurchase(pur_num)
            if not pur:
                messagebox.showerror("错误", "不存在该编号")
                return

            self.admin = Purchaser(pur)
            login_success[0] = True
            login_window.destroy()

        ttk.Button(input_frame, text="登录", command=try_login).pack(pady=20)

        login_window.transient(self.window)
        login_window.grab_set()
        self.window.wait_window(login_window)

        return login_success[0]

    def create_main_menu(self):
        # 创建主菜单框架
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.grid(row=0, column=0, sticky="nsew")

        # 创建按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(expand=True, fill="both", pady=20)

        # 创建按钮
        ttk.Button(button_frame, text="查询单个商品信息",
                   command=self.query_one_gui).pack(pady=5, fill="x")
        ttk.Button(button_frame, text="查询所有商品信息",
                   command=self.query_all_gui).pack(pady=5, fill="x")
        ttk.Button(button_frame, text="进货功能",
                   command=self.purchase_gui).pack(pady=5, fill="x")
        ttk.Button(button_frame, text="退出登录",
                   command=self.window.destroy).pack(pady=5, fill="x")

    def query_one_gui(self):
        com_num = simpledialog.askstring("查询商品", "请输入商品编号:")
        if not com_num:
            return

        res = Basic.queryOneCommodity(com_num)
        if not res:
            messagebox.showinfo("提示", "没有该商品")
        else:
            # 创建新窗口显示商品信息
            info_window = tk.Toplevel(self.window)
            info_window.title("商品信息")

            table = ttk.Treeview(info_window,
                                 columns=("商品编号", "商品名称", "商品类型", "规格", "单价",
                                          "生产日期", "过期日期", "库存数量"),
                                 show="headings")

            # 设置列标题
            for col in table["columns"]:
                table.heading(col, text=col)

            table.insert("", "end", values=res)
            table.pack(padx=10, pady=10)

    def query_all_gui(self):
        info = Basic.queryAllCommodity()

        # 创建新窗口显示所有商品信息
        info_window = tk.Toplevel(self.window)
        info_window.title("所有商品信息")

        # 创建表格
        table = ttk.Treeview(info_window,
                             columns=("商品编号", "商品名称", "商品类型", "规格", "单价",
                                      "生产日期", "过期日期", "库存数量"),
                             show="headings")

        # 设置列标题
        for col in table["columns"]:
            table.heading(col, text=col)

        # 添加数据
        for item in info:
            table.insert("", "end", values=item)

        # 添加滚动条
        scrollbar = ttk.Scrollbar(info_window,
                                  orient="vertical",
                                  command=table.yview)
        table.configure(yscrollcommand=scrollbar.set)

        table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def add_one_gui(self):
        # 创建输入窗口
        input_window = tk.Toplevel(self.window)
        input_window.title("添加商品")
        input_window.geometry("400x500")

        # 创建输入框
        ttk.Label(input_window, text="商品编号:").grid(row=0,
                                                   column=0,
                                                   padx=5,
                                                   pady=5)
        com_num_entry = ttk.Entry(input_window)
        com_num_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_window, text="商品名称:").grid(row=1,
                                                   column=0,
                                                   padx=5,
                                                   pady=5)
        com_name_entry = ttk.Entry(input_window)
        com_name_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(input_window, text="商品类型:").grid(row=2,
                                                   column=0,
                                                   padx=5,
                                                   pady=5)
        com_type_entry = ttk.Entry(input_window)
        com_type_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(input_window, text="规格:").grid(row=3,
                                                 column=0,
                                                 padx=5,
                                                 pady=5)
        com_size_entry = ttk.Entry(input_window)
        com_size_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(input_window, text="单价:").grid(row=4,
                                                 column=0,
                                                 padx=5,
                                                 pady=5)
        com_price_entry = ttk.Entry(input_window)
        com_price_entry.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(input_window, text="生产日期(年-月-日):").grid(row=5,
                                                          column=0,
                                                          padx=5,
                                                          pady=5)
        com_mdate_entry = ttk.Entry(input_window)
        com_mdate_entry.grid(row=5, column=1, padx=5, pady=5)

        ttk.Label(input_window, text="过期日期(年-月-日):").grid(row=6,
                                                          column=0,
                                                          padx=5,
                                                          pady=5)
        com_edate_entry = ttk.Entry(input_window)
        com_edate_entry.grid(row=6, column=1, padx=5, pady=5)

        def submit():
            try:
                com_num = com_num_entry.get().strip()
                com = Basic.queryOneCommodity(com_num)
                if com:
                    messagebox.showerror("错误", "该商品已存在不能重复添加")
                    return

                com_name = com_name_entry.get().strip()
                com_type = com_type_entry.get().strip()
                com_size = com_size_entry.get().strip()
                com_price = float(com_price_entry.get().strip())
                com_mdate = com_mdate_entry.get().strip()
                com_edate = com_edate_entry.get().strip()
                com_quantity = 0

                Basic.addOneCommodity(com_num, com_name, com_type, com_size,
                                      com_price, com_mdate, com_edate,
                                      com_quantity)
                messagebox.showinfo("成功", "添加成功")
                input_window.destroy()
            except Exception as e:
                messagebox.showerror("错误", f"添加失败: {str(e)}")

        ttk.Button(input_window, text="提交", command=submit).grid(row=7,
                                                                 column=0,
                                                                 columnspan=2,
                                                                 pady=20)

    def query_all_stock_gui(self):
        info = Basic.queryAllStock()

        # 创建新窗口显示所有进货信息
        info_window = tk.Toplevel(self.window)
        info_window.title("所有进货信息")

        # 创建表格
        table = ttk.Treeview(info_window,
                             columns=("进货员编号", "商品编号", "进货流水号", "进货单价", "增加数量",
                                      "进货日期"),
                             show="headings")

        # 设置列标题
        for col in table["columns"]:
            table.heading(col, text=col)

        # 添加数据
        for item in info:
            table.insert("", "end", values=item)

        # 添加滚动条
        scrollbar = ttk.Scrollbar(info_window,
                                  orient="vertical",
                                  command=table.yview)
        table.configure(yscrollcommand=scrollbar.set)

        table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def purchase_gui(self):
        # 创建输入窗口
        input_window = tk.Toplevel(self.window)
        input_window.title("进货")
        input_window.geometry("300x300")

        # 创建输入框
        ttk.Label(input_window, text="商品编号:").grid(row=0,
                                                   column=0,
                                                   padx=5,
                                                   pady=5)
        com_num_entry = ttk.Entry(input_window)
        com_num_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_window, text="进货数量:").grid(row=1,
                                                   column=0,
                                                   padx=5,
                                                   pady=5)
        com_cnt_entry = ttk.Entry(input_window)
        com_cnt_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(input_window, text="进货单价:").grid(row=2,
                                                   column=0,
                                                   padx=5,
                                                   pady=5)
        com_price_entry = ttk.Entry(input_window)
        com_price_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(input_window, text="进货日期(年-月-日):").grid(row=3,
                                                          column=0,
                                                          padx=5,
                                                          pady=5)
        in_date_entry = ttk.Entry(input_window)
        in_date_entry.grid(row=3, column=1, padx=5, pady=5)

        def submit():
            try:
                com_num = com_num_entry.get().strip()
                com = Basic.queryOneCommodity(com_num)
                if not com:
                    messagebox.showerror("错误", "该商品不存在，请先添加该商品")
                    return

                com_cnt = int(com_cnt_entry.get().strip())
                com_price = float(com_price_entry.get().strip())
                in_date = in_date_entry.get().strip()

                num = self.getFlowNum()
                Basic.addOneStock(self.admin.getNo(), com_num, num, com_price,
                                  com_cnt, in_date)
                Basic.addOneCommodityCnt(com_num, com_cnt)
                messagebox.showinfo("成功", "操作成功")
                input_window.destroy()
            except Exception as e:
                messagebox.showerror("错误", f"操作失败: {str(e)}")

        ttk.Button(input_window, text="提交", command=submit).grid(row=4,
                                                                 column=0,
                                                                 columnspan=2,
                                                                 pady=20)

    def querAllStock(self):
        generaloperat.queryAllStock()

    def addOne(self):
        '''前台 添加一个新的商品，库存数量为0'''
        com_num = input("请输入要添加的商品编号:").strip()
        com = Basic.queryOneCommodity(com_num)
        if com != []:
            print("该商品已存在不能重复添加.")
            return
        com_name = input("请输入商品名称:").strip()
        com_type = input("请输入商品类型:").strip()
        com_size = input("请输入规格:").strip()
        com_price = float(input("请输入单价:").strip())
        com_mdate = input("请输入生产日期(格式 年-月-日):").strip()
        com_edate = input("请输入过期日期(格式 年-月-日):").strip()
        com_quantity = 0
        try:
            Basic.addOneCommodity(com_num, com_name, com_type, com_size,
                                  com_price, com_mdate, com_edate,
                                  com_quantity)
            print("添加成功")
        except Exception as e:
            print("添加失败,原因：", e)

    def purchase(self):
        '''前台 进货'''
        com_num = input("请输入要进货的商品编号:").strip()
        com = Basic.queryOneCommodity(com_num)
        if com == []:
            print("该商品不存在，请先添加该商品.")
            return
        com_cnt = int(input("请输入进货的数量:").strip())
        com_price = float(input("请输入进货的单价:").strip())
        in_date = input("请输入进货日期(格式 年-月-日):").strip()
        try:
            num = self.getFlowNum()
            Basic.addOneStock(self.admin.getNo(), com_num, num, com_price,
                              com_cnt, in_date)
            Basic.addOneCommodityCnt(com_num, com_cnt)
            print("操作成功.")
        except Exception as e:
            print("操作失败，原因：", e)

    def queryAll(self):
        '''前台 查看所有商品信息'''
        generaloperat.queryAllCommodity()

    def queryOne(self):
        '''前台 查看一个商品信息'''
        generaloperat.queryOneCommodity()

    def exitlogin(self):
        '''前台 退出登陆 ，保证已经登陆'''
        self.admin = None

    def getFlowNum(self):
        while True:
            num = Basic.getFlowNum()
            info = Basic.queryOneStockFlowNum(num)
            if info == []:
                return num
