import generaloperat
from basic import Basic
from commodity import Commodity
from purchaser import Purchaser
from admin import Admin
import os
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import simpledialog


class AdminManage:

    def __init__(self):
        self.admin = None
        self.window = None

    def show_gui(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("管理员界面")
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

        ttk.Label(input_frame, text="管理员账号:").pack(pady=5)
        username_entry = ttk.Entry(input_frame, width=20)
        username_entry.pack(pady=5)

        ttk.Label(input_frame, text="密码:").pack(pady=5)
        password_entry = ttk.Entry(input_frame, show="*", width=20)
        password_entry.pack(pady=5)

        login_success = [False]

        def try_login():
            admin_no = username_entry.get().strip()
            adm = Basic.queryOneAdmin(admin_no)
            if not adm:
                messagebox.showerror("错误", "不存在该账号")
                return

            admin = Admin(adm)
            in_pwd = password_entry.get().strip()
            if admin.getPwd() == in_pwd:
                self.admin = admin
                login_success[0] = True
                login_window.destroy()
            else:
                messagebox.showerror("错误", "密码错误")

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
        ttk.Button(button_frame, text="查询菜单",
                   command=self.create_query_menu).pack(pady=5, fill="x")
        ttk.Button(button_frame, text="添加菜单",
                   command=self.create_add_menu).pack(pady=5, fill="x")
        ttk.Button(button_frame, text="删除菜单",
                   command=self.create_delete_menu).pack(pady=5, fill="x")
        ttk.Button(button_frame, text="修改菜单",
                   command=self.create_modify_menu).pack(pady=5, fill="x")
        ttk.Button(button_frame, text="销量统计",
                   command=self.statistic_gui).pack(pady=5, fill="x")
        ttk.Button(button_frame, text="退出登录",
                   command=self.window.destroy).pack(pady=5, fill="x")

    def create_query_menu(self):
        query_window = tk.Toplevel(self.window)
        query_window.title("查询菜单")
        query_window.geometry("300x400")

        ttk.Button(query_window,
                   text="查看所有商品信息",
                   command=self.query_all_commodity_gui).grid(row=0,
                                                              column=0,
                                                              pady=5,
                                                              padx=5)
        ttk.Button(query_window,
                   text="查看所有售货员信息",
                   command=self.query_all_cashier_gui).grid(row=1,
                                                            column=0,
                                                            pady=5,
                                                            padx=5)
        ttk.Button(query_window,
                   text="查看所有进货员信息",
                   command=self.query_all_purchaser_gui).grid(row=2,
                                                              column=0,
                                                              pady=5,
                                                              padx=5)
        ttk.Button(query_window,
                   text="查看所有售货信息",
                   command=self.query_all_sell_gui).grid(row=3,
                                                         column=0,
                                                         pady=5,
                                                         padx=5)
        ttk.Button(query_window,
                   text="查看所有进货信息",
                   command=self.query_all_stock_gui).grid(row=4,
                                                          column=0,
                                                          pady=5,
                                                          padx=5)

    def create_add_menu(self):
        add_window = tk.Toplevel(self.window)
        add_window.title("添加菜单")
        add_window.geometry("300x200")

        ttk.Button(add_window, text="增加新的售货员",
                   command=self.add_cashier_gui).grid(row=0,
                                                      column=0,
                                                      pady=5,
                                                      padx=5)
        ttk.Button(add_window, text="增加新的进货员",
                   command=self.add_purchaser_gui).grid(row=1,
                                                        column=0,
                                                        pady=5,
                                                        padx=5)
        ttk.Button(add_window, text="增加新的商品",
                   command=self.add_commodity_gui).grid(row=2,
                                                        column=0,
                                                        pady=5,
                                                        padx=5)

    def create_delete_menu(self):
        delete_window = tk.Toplevel(self.window)
        delete_window.title("删除菜单")
        delete_window.geometry("300x200")

        ttk.Button(delete_window,
                   text="移除一个售货员",
                   command=self.delete_cashier_gui).grid(row=0,
                                                         column=0,
                                                         pady=5,
                                                         padx=5)
        ttk.Button(delete_window,
                   text="移除一个进货员",
                   command=self.delete_purchaser_gui).grid(row=1,
                                                           column=0,
                                                           pady=5,
                                                           padx=5)
        ttk.Button(delete_window,
                   text="移除一个商品",
                   command=self.delete_commodity_gui).grid(row=2,
                                                           column=0,
                                                           pady=5,
                                                           padx=5)

    def create_modify_menu(self):
        modify_window = tk.Toplevel(self.window)
        modify_window.title("修改菜单")
        modify_window.geometry("300x200")

        ttk.Button(modify_window,
                   text="修改售货员信息",
                   command=self.modify_cashier_gui).grid(row=0,
                                                         column=0,
                                                         pady=5,
                                                         padx=5)
        ttk.Button(modify_window,
                   text="修改进货员信息",
                   command=self.modify_purchaser_gui).grid(row=1,
                                                           column=0,
                                                           pady=5,
                                                           padx=5)
        ttk.Button(modify_window,
                   text="修改商品信息",
                   command=self.modify_commodity_gui).grid(row=2,
                                                           column=0,
                                                           pady=5,
                                                           padx=5)

    def query_all_commodity_gui(self):
        info = Basic.queryAllCommodity()
        self.show_table_window(
            "所有商品信息", info,
            ("商品编号", "商品名称", "商品类型", "规格", "单价", "生产日期", "过期日期", "库存数量"))

    def query_all_cashier_gui(self):
        info = Basic.queryAllCashier()
        self.show_table_window(
            "所有售货员信息", info,
            ("售货员编号", "姓名", "密码", "性别", "年龄", "Hourse", "工资/月", "手机号", "出生日期"))

    def query_all_purchaser_gui(self):
        info = Basic.queryAllPurchaser()
        self.show_table_window(
            "所有进货员信息", info,
            ("进货员编号", "姓名", "性别", "年龄", "工资/月", "手机号", "出生日期"))

    def query_all_sell_gui(self):
        info = Basic.queryAllSell()
        self.show_table_window("所有售货信息", info,
                               ("收银员编号", "商品编号", "出售流水号", "出售数量", "总价", "日期"))

    def query_all_stock_gui(self):
        info = Basic.queryAllStock()
        self.show_table_window(
            "所有进货信息", info, ("进货员编号", "商品编号", "进货流水号", "进货单价", "增加数量", "进货日期"))

    def show_table_window(self, title, data, columns):
        window = tk.Toplevel(self.window)
        window.title(title)

        # 创建表格
        table = ttk.Treeview(window, columns=columns, show="headings")

        # 设置列标题
        for col in columns:
            table.heading(col, text=col)

        # 添加数据
        for item in data:
            table.insert("", "end", values=item)

        # 添加滚动条
        scrollbar = ttk.Scrollbar(window,
                                  orient="vertical",
                                  command=table.yview)
        table.configure(yscrollcommand=scrollbar.set)

        table.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def add_cashier_gui(self):
        input_window = tk.Toplevel(self.window)
        input_window.title("添加售货员")
        input_window.geometry("400x500")

        # 创建输入框
        ttk.Label(input_window, text="售货员编号:").grid(row=0,
                                                    column=0,
                                                    padx=5,
                                                    pady=5)
        cash_no_entry = ttk.Entry(input_window)
        cash_no_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_window, text="姓名:").grid(row=1,
                                                 column=0,
                                                 padx=5,
                                                 pady=5)
        cash_name_entry = ttk.Entry(input_window)
        cash_name_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(input_window, text="密码:").grid(row=2,
                                                 column=0,
                                                 padx=5,
                                                 pady=5)
        cash_pwd_entry = ttk.Entry(input_window)
        cash_pwd_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(input_window, text="性别:").grid(row=3,
                                                 column=0,
                                                 padx=5,
                                                 pady=5)
        cash_sex_entry = ttk.Entry(input_window)
        cash_sex_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(input_window, text="年龄:").grid(row=4,
                                                 column=0,
                                                 padx=5,
                                                 pady=5)
        cash_age_entry = ttk.Entry(input_window)
        cash_age_entry.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(input_window, text="日工作量:").grid(row=5,
                                                   column=0,
                                                   padx=5,
                                                   pady=5)
        cash_hourse_entry = ttk.Entry(input_window)
        cash_hourse_entry.grid(row=5, column=1, padx=5, pady=5)

        ttk.Label(input_window, text="月工资:").grid(row=6,
                                                  column=0,
                                                  padx=5,
                                                  pady=5)
        cash_salary_entry = ttk.Entry(input_window)
        cash_salary_entry.grid(row=6, column=1, padx=5, pady=5)

        ttk.Label(input_window, text="手机号:").grid(row=7,
                                                  column=0,
                                                  padx=5,
                                                  pady=5)
        cash_phone_entry = ttk.Entry(input_window)
        cash_phone_entry.grid(row=7, column=1, padx=5, pady=5)

        ttk.Label(input_window, text="出生日期(年-月-日):").grid(row=8,
                                                          column=0,
                                                          padx=5,
                                                          pady=5)
        cash_entry_entry = ttk.Entry(input_window)
        cash_entry_entry.grid(row=8, column=1, padx=5, pady=5)

        def submit():
            try:
                cash_no = cash_no_entry.get().strip()
                cash = Basic.queryOneCashier(cash_no)
                if cash:
                    messagebox.showerror("错误", "该编号已存在不能重复添加")
                    return

                cash_name = cash_name_entry.get().strip()
                cash_pwd = cash_pwd_entry.get().strip()
                cash_sex = cash_sex_entry.get().strip()
                cash_age = int(cash_age_entry.get().strip())
                cash_hourse = float(cash_hourse_entry.get().strip())
                cash_salary = float(cash_salary_entry.get().strip())
                cash_phone = cash_phone_entry.get().strip()
                cash_entry = cash_entry_entry.get().strip()

                Basic.addOneCashier(cash_no, cash_name, cash_pwd, cash_sex,
                                    cash_age, cash_hourse, cash_salary,
                                    cash_phone, cash_entry)
                messagebox.showinfo("成功", "添加售货员成功")
                input_window.destroy()
            except Exception as e:
                messagebox.showerror("错误", f"添加失败: {str(e)}")

        ttk.Button(input_window, text="提交", command=submit).grid(row=9,
                                                                 column=0,
                                                                 columnspan=2,
                                                                 pady=20)

    def add_purchaser_gui(self):
        input_window = tk.Toplevel(self.window)
        input_window.title("添加进货员")
        input_window.geometry("400x400")

        # 创建输入框
        ttk.Label(input_window, text="进货员编号:").grid(row=0,
                                                    column=0,
                                                    padx=5,
                                                    pady=5)
        pur_no_entry = ttk.Entry(input_window)
        pur_no_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_window, text="姓名:").grid(row=1,
                                                 column=0,
                                                 padx=5,
                                                 pady=5)
        pur_name_entry = ttk.Entry(input_window)
        pur_name_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(input_window, text="性别:").grid(row=2,
                                                 column=0,
                                                 padx=5,
                                                 pady=5)
        pur_sex_entry = ttk.Entry(input_window)
        pur_sex_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(input_window, text="年龄:").grid(row=3,
                                                 column=0,
                                                 padx=5,
                                                 pady=5)
        pur_age_entry = ttk.Entry(input_window)
        pur_age_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(input_window, text="月工资:").grid(row=4,
                                                  column=0,
                                                  padx=5,
                                                  pady=5)
        pur_salary_entry = ttk.Entry(input_window)
        pur_salary_entry.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(input_window, text="手机号:").grid(row=5,
                                                  column=0,
                                                  padx=5,
                                                  pady=5)
        pur_phone_entry = ttk.Entry(input_window)
        pur_phone_entry.grid(row=5, column=1, padx=5, pady=5)

        ttk.Label(input_window, text="出生日期(年-月-日):").grid(row=6,
                                                          column=0,
                                                          padx=5,
                                                          pady=5)
        pur_entry_entry = ttk.Entry(input_window)
        pur_entry_entry.grid(row=6, column=1, padx=5, pady=5)

        def submit():
            try:
                pur_no = pur_no_entry.get().strip()
                pur = Basic.queryOnePurchase(pur_no)
                if pur:
                    messagebox.showerror("错误", "该编号已存在不能重复添加")
                    return

                pur_name = pur_name_entry.get().strip()
                pur_sex = pur_sex_entry.get().strip()
                pur_age = int(pur_age_entry.get().strip())
                pur_salary = float(pur_salary_entry.get().strip())
                pur_phone = pur_phone_entry.get().strip()
                pur_entry = pur_entry_entry.get().strip()

                Basic.addOnePurchaser(pur_no, pur_name, pur_sex, pur_age,
                                      pur_salary, pur_phone, pur_entry)
                messagebox.showinfo("成功", "添加进货员成功")
                input_window.destroy()
            except Exception as e:
                messagebox.showerror("错误", f"添加失败: {str(e)}")

        ttk.Button(input_window, text="提交", command=submit).grid(row=7,
                                                                 column=0,
                                                                 columnspan=2,
                                                                 pady=20)

    def add_commodity_gui(self):
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

        ttk.Label(input_window, text="库存数量:").grid(row=7,
                                                   column=0,
                                                   padx=5,
                                                   pady=5)
        com_quantity_entry = ttk.Entry(input_window)
        com_quantity_entry.grid(row=7, column=1, padx=5, pady=5)

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
                com_quantity = int(com_quantity_entry.get().strip())

                Basic.addOneCommodity(com_num, com_name, com_type, com_size,
                                      com_price, com_mdate, com_edate,
                                      com_quantity)
                messagebox.showinfo("成功", "添加商品成功")
                input_window.destroy()
            except Exception as e:
                messagebox.showerror("错误", f"添加失败: {str(e)}")

        ttk.Button(input_window, text="提交", command=submit).grid(row=8,
                                                                 column=0,
                                                                 columnspan=2,
                                                                 pady=20)

    def delete_cashier_gui(self):
        cash_no = simpledialog.askstring("删除售货员", "请输入要删除的售货员编号:")
        if not cash_no:
            return

        cash = Basic.queryOneCashier(cash_no)
        if not cash:
            messagebox.showerror("错误", "不存在该员工")
            return

        if messagebox.askyesno("确认", "确认删除该售货员？(删除后所有与该员工有关的售货记录都会删除)"):
            try:
                Basic.delOneCashier(cash_no)
                messagebox.showinfo("成功", "删除成功")
            except Exception as e:
                messagebox.showerror("错误", f"删除失败: {str(e)}")

    def delete_purchaser_gui(self):
        pur_no = simpledialog.askstring("删除进货员", "请输入要删除的进货员编号:")
        if not pur_no:
            return

        pur = Basic.queryOnePurchase(pur_no)
        if not pur:
            messagebox.showerror("错误", "不存在该员工")
            return

        if messagebox.askyesno("确认", "确认删除该进货员？(删除后所有与该员工有关的进货记录都会删除)"):
            try:
                Basic.delOnePurchase(pur_no)
                messagebox.showinfo("成功", "删除成功")
            except Exception as e:
                messagebox.showerror("错误", f"删除失败: {str(e)}")

    def delete_commodity_gui(self):
        com_no = simpledialog.askstring("删除商品", "请输入要删除的商品编号:")
        if not com_no:
            return

        com = Basic.queryOneCommodity(com_no)
        if not com:
            messagebox.showerror("错误", "不存在该商品")
            return

        if messagebox.askyesno("确认", "确认删除该商品？(删除后所有与该商品有关的进出货记录都会删除)"):
            try:
                Basic.delOneCommodity(com_no)
                messagebox.showinfo("成功", "删除成功")
            except Exception as e:
                messagebox.showerror("错误", f"删除失败: {str(e)}")

    def modify_cashier_gui(self):
        cash_no = simpledialog.askstring("修改售货员", "请输入需要修改的售货员编号:")
        if not cash_no:
            return

        cash = Basic.queryOneCashier(cash_no)
        if not cash:
            messagebox.showerror("错误", "该售货员不存在")
            return

        input_window = tk.Toplevel(self.window)
        input_window.title("修改售货员信息")
        input_window.geometry("400x500")

        # 创建输入框
        ttk.Label(input_window, text="姓名:").grid(row=0,
                                                 column=0,
                                                 padx=5,
                                                 pady=5)
        cash_name_entry = ttk.Entry(input_window)
        cash_name_entry.insert(0, cash[1])
        cash_name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_window, text="密码:").grid(row=1,
                                                 column=0,
                                                 padx=5,
                                                 pady=5)
        cash_pwd_entry = ttk.Entry(input_window)
        cash_pwd_entry.insert(0, cash[2])
        cash_pwd_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(input_window, text="性别:").grid(row=2,
                                                 column=0,
                                                 padx=5,
                                                 pady=5)
        cash_sex_entry = ttk.Entry(input_window)
        cash_sex_entry.insert(0, cash[3])
        cash_sex_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(input_window, text="年龄:").grid(row=3,
                                                 column=0,
                                                 padx=5,
                                                 pady=5)
        cash_age_entry = ttk.Entry(input_window)
        cash_age_entry.insert(0, cash[4])
        cash_age_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(input_window, text="日工作量:").grid(row=4,
                                                   column=0,
                                                   padx=5,
                                                   pady=5)
        cash_hourse_entry = ttk.Entry(input_window)
        cash_hourse_entry.insert(0, cash[5])
        cash_hourse_entry.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(input_window, text="月工资:").grid(row=5,
                                                  column=0,
                                                  padx=5,
                                                  pady=5)
        cash_salary_entry = ttk.Entry(input_window)
        cash_salary_entry.insert(0, cash[6])
        cash_salary_entry.grid(row=5, column=1, padx=5, pady=5)

        ttk.Label(input_window, text="手机号:").grid(row=6,
                                                  column=0,
                                                  padx=5,
                                                  pady=5)
        cash_phone_entry = ttk.Entry(input_window)
        cash_phone_entry.insert(0, cash[7])
        cash_phone_entry.grid(row=6, column=1, padx=5, pady=5)

        ttk.Label(input_window, text="出生日期(年-月-日):").grid(row=7,
                                                          column=0,
                                                          padx=5,
                                                          pady=5)
        cash_entry_entry = ttk.Entry(input_window)
        cash_entry_entry.insert(0, cash[8])
        cash_entry_entry.grid(row=7, column=1, padx=5, pady=5)

        def submit():
            try:
                cash_name = cash_name_entry.get().strip()
                cash_pwd = cash_pwd_entry.get().strip()
                cash_sex = cash_sex_entry.get().strip()
                cash_age = int(cash_age_entry.get().strip())
                cash_hourse = float(cash_hourse_entry.get().strip())
                cash_salary = float(cash_salary_entry.get().strip())
                cash_phone = cash_phone_entry.get().strip()
                cash_entry = cash_entry_entry.get().strip()

                Basic.modifyOneCashier(cash_no, cash_name, cash_pwd, cash_sex,
                                       cash_age, cash_hourse, cash_salary,
                                       cash_phone, cash_entry)
                messagebox.showinfo("成功", "修改成功")
                input_window.destroy()
            except Exception as e:
                messagebox.showerror("错误", f"修改失败: {str(e)}")

        ttk.Button(input_window, text="提交", command=submit).grid(row=8,
                                                                 column=0,
                                                                 columnspan=2,
                                                                 pady=20)

    def modify_purchaser_gui(self):
        pur_no = simpledialog.askstring("修改进货员", "请输入需要修改的进货员编号:")
        if not pur_no:
            return

        pur = Basic.queryOnePurchase(pur_no)
        if not pur:
            messagebox.showerror("错误", "该进货员不存在")
            return

        input_window = tk.Toplevel(self.window)
        input_window.title("修改进货员信息")
        input_window.geometry("400x400")

        # 创建输入框
        ttk.Label(input_window, text="姓名:").grid(row=0,
                                                 column=0,
                                                 padx=5,
                                                 pady=5)
        pur_name_entry = ttk.Entry(input_window)
        pur_name_entry.insert(0, pur[1])
        pur_name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_window, text="性别:").grid(row=1,
                                                 column=0,
                                                 padx=5,
                                                 pady=5)
        pur_sex_entry = ttk.Entry(input_window)
        pur_sex_entry.insert(0, pur[2])
        pur_sex_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(input_window, text="年龄:").grid(row=2,
                                                 column=0,
                                                 padx=5,
                                                 pady=5)
        pur_age_entry = ttk.Entry(input_window)
        pur_age_entry.insert(0, pur[3])
        pur_age_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(input_window, text="月工资:").grid(row=3,
                                                  column=0,
                                                  padx=5,
                                                  pady=5)
        pur_salary_entry = ttk.Entry(input_window)
        pur_salary_entry.insert(0, pur[4])
        pur_salary_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(input_window, text="手机号:").grid(row=4,
                                                  column=0,
                                                  padx=5,
                                                  pady=5)
        pur_phone_entry = ttk.Entry(input_window)
        pur_phone_entry.insert(0, pur[5])
        pur_phone_entry.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(input_window, text="出生日期(年-月-日):").grid(row=5,
                                                          column=0,
                                                          padx=5,
                                                          pady=5)
        pur_entry_entry = ttk.Entry(input_window)
        pur_entry_entry.insert(0, pur[6])
        pur_entry_entry.grid(row=5, column=1, padx=5, pady=5)

        def submit():
            try:
                pur_name = pur_name_entry.get().strip()
                pur_sex = pur_sex_entry.get().strip()
                pur_age = int(pur_age_entry.get().strip())
                pur_salary = float(pur_salary_entry.get().strip())
                pur_phone = pur_phone_entry.get().strip()
                pur_entry = pur_entry_entry.get().strip()

                Basic.modifyOnePurchaser(pur_no, pur_name, pur_sex, pur_age,
                                         pur_salary, pur_phone, pur_entry)
                messagebox.showinfo("成功", "修改成功")
                input_window.destroy()
            except Exception as e:
                messagebox.showerror("错误", f"修改失败: {str(e)}")

        ttk.Button(input_window, text="提交", command=submit).grid(row=6,
                                                                 column=0,
                                                                 columnspan=2,
                                                                 pady=20)

    def modify_commodity_gui(self):
        com_num = simpledialog.askstring("修改商品", "请输入要修改的商品编号:")
        if not com_num:
            return

        com = Basic.queryOneCommodity(com_num)
        if not com:
            messagebox.showerror("错误", "该商品不存在")
            return

        input_window = tk.Toplevel(self.window)
        input_window.title("修改商品信息")
        input_window.geometry("400x500")

        # 创建输入框
        ttk.Label(input_window, text="商品名称:").grid(row=0,
                                                   column=0,
                                                   padx=5,
                                                   pady=5)
        com_name_entry = ttk.Entry(input_window)
        com_name_entry.insert(0, com[1])
        com_name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_window, text="商品类型:").grid(row=1,
                                                   column=0,
                                                   padx=5,
                                                   pady=5)
        com_type_entry = ttk.Entry(input_window)
        com_type_entry.insert(0, com[2])
        com_type_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(input_window, text="规格:").grid(row=2,
                                                 column=0,
                                                 padx=5,
                                                 pady=5)
        com_size_entry = ttk.Entry(input_window)
        com_size_entry.insert(0, com[3])
        com_size_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(input_window, text="单价:").grid(row=3,
                                                 column=0,
                                                 padx=5,
                                                 pady=5)
        com_price_entry = ttk.Entry(input_window)
        com_price_entry.insert(0, com[4])
        com_price_entry.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(input_window, text="生产日期(年-月-日):").grid(row=4,
                                                          column=0,
                                                          padx=5,
                                                          pady=5)
        com_mdate_entry = ttk.Entry(input_window)
        com_mdate_entry.insert(0, com[5])
        com_mdate_entry.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(input_window, text="过期日期(年-月-日):").grid(row=5,
                                                          column=0,
                                                          padx=5,
                                                          pady=5)
        com_edate_entry = ttk.Entry(input_window)
        com_edate_entry.insert(0, com[6])
        com_edate_entry.grid(row=5, column=1, padx=5, pady=5)

        ttk.Label(input_window, text="库存数量:").grid(row=6,
                                                   column=0,
                                                   padx=5,
                                                   pady=5)
        com_quantity_entry = ttk.Entry(input_window)
        com_quantity_entry.insert(0, com[7])
        com_quantity_entry.grid(row=6, column=1, padx=5, pady=5)

        def submit():
            try:
                com_name = com_name_entry.get().strip()
                com_type = com_type_entry.get().strip()
                com_size = com_size_entry.get().strip()
                com_price = float(com_price_entry.get().strip())
                com_mdate = com_mdate_entry.get().strip()
                com_edate = com_edate_entry.get().strip()
                com_quantity = int(com_quantity_entry.get().strip())

                Basic.modifyOneCommodity(com_num, com_name, com_type, com_size,
                                         com_price, com_mdate, com_edate,
                                         com_quantity)
                messagebox.showinfo("成功", "修改商品成功")
                input_window.destroy()
            except Exception as e:
                messagebox.showerror("错误", f"修改失败: {str(e)}")

        ttk.Button(input_window, text="提交", command=submit).grid(row=7,
                                                                 column=0,
                                                                 columnspan=2,
                                                                 pady=20)

    def statistic_gui(self):
        input_window = tk.Toplevel(self.window)
        input_window.title("销量统计")
        input_window.geometry("300x200")

        ttk.Label(input_window, text="开始日期(年-月-日):").grid(row=0,
                                                          column=0,
                                                          padx=5,
                                                          pady=5)
        left_entry = ttk.Entry(input_window)
        left_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(input_window, text="结束日期(年-月-日):").grid(row=1,
                                                          column=0,
                                                          padx=5,
                                                          pady=5)
        right_entry = ttk.Entry(input_window)
        right_entry.grid(row=1, column=1, padx=5, pady=5)

        def submit():
            try:
                left = left_entry.get().strip()
                right = right_entry.get().strip()

                # 创建新窗口显示统计结果
                result_window = tk.Toplevel(input_window)
                result_window.title("销量统计结果")

                # 创建表格
                table = ttk.Treeview(result_window,
                                     columns=("销量排行", "商品编号", "商品名称", "类型",
                                              "单价", "指定日期内销量"),
                                     show="headings")

                # 设置列标题
                for col in table["columns"]:
                    table.heading(col, text=col)

                # 获取统计数据
                cnt_list = generaloperat.getBothTopStatic(left, right, 10)

                # 添加数据
                for i, item in enumerate(cnt_list[:10]):
                    table.insert("",
                                 "end",
                                 values=(i + 1, item.ob.getNo(),
                                         item.ob.getName(), item.ob.getType(),
                                         item.ob.getPrice(), item.cnt))

                # 添加滚动条
                scrollbar = ttk.Scrollbar(result_window,
                                          orient="vertical",
                                          command=table.yview)
                table.configure(yscrollcommand=scrollbar.set)

                table.pack(side="left", fill="both", expand=True)
                scrollbar.pack(side="right", fill="y")

                input_window.destroy()
            except Exception as e:
                messagebox.showerror("错误", f"统计失败: {str(e)}")

        ttk.Button(input_window, text="统计", command=submit).grid(row=2,
                                                                 column=0,
                                                                 columnspan=2,
                                                                 pady=20)

    # ... 保留原有的其他方法 ...
