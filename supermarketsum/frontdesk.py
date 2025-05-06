from basic import Basic
from commodity import Commodity
from prettytable import PrettyTable
from cashier import Cashier
import os
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import simpledialog


class ShopCar:
    '''储存商品对象和购买数量
    '''

    def __init__(self):
        self.shop_list = []

    def addCommodity(self, com, com_cnt):  #传入商品信息和购买数量
        ''' *保证库存肯定是有货的
        商品重复则直接添加数量,否则添加到列表即可
        '''
        com_no = com.getNo()
        for i in range(len(self.shop_list)):
            now_com = self.shop_list[i][0]
            if now_com.getNo() == com_no:
                self.shop_list[i][1] += com_cnt
                return
        #购物车不存在该商品
        self.shop_list.append([com, com_cnt])
        return

    def delCommodity(self, com_num, com_cnt):
        '''保证满足
        '''
        for i in range(len(self.shop_list)):
            now_com = self.shop_list[i][0]
            if now_com.getNo() == com_num:
                self.shop_list[i][1] -= com_cnt
                if self.shop_list[i][1] == 0:
                    self.shop_list.pop(i)
                return

    def clear(self):
        '''清空购物车'''
        self.shop_list.clear()

    def getMonery(self):
        '''得到总钱数'''
        res = 0.0
        for com, cnt in self.shop_list:
            res += com.getPrice() * cnt
        return res

    def getCommodityCnt(self, com_num):
        '''返回商品编号对应的数量'''
        res = 0
        for com, cnt in self.shop_list:
            if com.getNo() == com_num:
                res = cnt
                break
        return res

    def printList(self):
        '''打印当前购物车信息
        ["商品编号", "商品名称", "商品类型","规格","单价","购买数量"]
        '''
        table = PrettyTable(["商品编号", "商品名称", "商品类型", "规格", "单价", "购买数量"])
        for com, cnt in self.shop_list:
            table.add_row([
                com.getNo(),
                com.getName(),
                com.getType(),
                com.getSize(),
                com.getPrice(), cnt
            ])
        print(table)
        print("总价：", self.getMonery(), end="\n\n")

    def getlist(self):
        ''' 返回购买信息'''
        # res_list=[]
        # for i in self.shop_list:
        #     com=i[0]
        #     cnt=i[2]
        #     res_list.append((com.getNo(),cnt))#返回商品编号和 购买的数量
        # return res_list
        return self.shop_list

    def empty(self):
        if not self.shop_list:
            return True
        return False


class FrontDesk:
    '''前台控制'''

    def __init__(self):
        self.admin = None
        self.car = ShopCar()
        self.window = None

    def exitLogin(self):
        print("账号 {} 已经退出登陆.".format(self.admin.getNo()))
        self.admin = None

    def meta(self):
        '''前台:菜单'''
        if self.login() == False:
            return
        while (True):
            os.system("cls")
            print("------------------------------------------------")
            print("1: 查询单个商品信息")
            print("2: 查看所有商品信息")
            print("3: 购买功能")
            if self.admin != None:
                print("4: 退出登录")
            print("                                     其他数字退出")
            print("------------------------------------------------")
            cmd = input("请输入选项:").strip()
            if cmd == "1":
                self.queryOne()
            elif cmd == "2":
                self.queryAll()
            elif cmd == "3":
                if (self.admin != None) or self.login():
                    self.shopingMeta()
            elif self.admin != None and cmd == "4":
                self.exitLogin()
                break
            else:
                break
            os.system("pause")

    def login(self):
        '''前台:admin登陆'''
        in_num = input("请输入您的账号:").strip()
        cash = Basic.queryOneCashier(in_num)
        if not cash:
            print("不存在该账号.")
            return False
        cashier = Cashier(cash)
        in_pwd = input("请输入您的密码:").strip()
        if cashier.getPwd() == in_pwd:
            self.admin = cashier
            print("登陆成功.")
            return True
        else:
            print("密码错误.")
            return False

    def queryAll(self):
        '''前台:查询所有商品信息'''
        info = Basic.queryAllCommodity()
        table = comm = Commodity.getTableaHead()
        for i in info:
            table.add_row(i)
        print(table)
        print("以上共 {} 条记录.".format(len(info)))

    def queryOne(self):
        '''前台：查询一个商品信息'''
        com_num = input("请输入需要查询商品的编号:")
        res = Basic.queryOneCommodity(com_num)
        if not res:  #res为空
            print("没有该商品")
        else:
            table = comm = Commodity.getTableaHead()
            table.add_row(res)
            print(table, end="\n\n")

    def shopingMeta(self):
        '''前台：购买'''
        while True:
            os.system("cls")
            print("当前购物车:")
            self.car.printList()
            print("-------\n")
            print("1:向购物车中添加商品")
            print("2:从购物车中删除商品")
            print("3:清空购物车")
            print("4:结算")
            print("--------------------其他选项退出")
            cmd = input("请输入选项:").strip()
            if cmd == "1":
                self.addCom()
            elif cmd == "2":
                self.delCom()
            elif cmd == "3":
                self.clearShopCar()
            elif cmd == "4":
                self.pay()
            else:
                break
            os.system("pause")

    def addCom(self):
        '''前台: 添加购物车 '''
        com_num = input("请输入商品编号:").strip()
        com_info = Basic.queryOneCommodity(com_num)
        if not com_info:
            print("商品不存在.")
            return
        com = Commodity(com_info)
        com_cnt = int(input("请输入商品数量:").strip())
        if com_cnt <= 0:
            print("购买数量必须大于0.")
            return
        if com_cnt > com.getQuantiy():
            print("商品库存不足.")
        else:
            self.car.addCommodity(com, com_cnt)
            print("添加进入购物车成功.")

    def clearShopCar(self):
        '''前台：清空购物车'''
        cmd = input("输入 1 确认清空购物车:").strip()
        if cmd == "1":
            self.car.clear()
            print("购物车已清空.")
        else:
            print("操作已取消.")

    def delCom(self):
        '''前台：删除购物车某一个物品'''
        com_num = input("请输入商品编号:").strip()
        have_cnt = self.car.getCommodityCnt(com_num)
        if have_cnt == 0:
            print("购物车中无该商品")
        else:
            del_cnt = int(
                input("购物车中该商品有 {} 个,请输入需要删除该商品的数量:".format(have_cnt)).strip())
            self.car.delCommodity(com_num, min(del_cnt, have_cnt))
            print("删除成功.")

    def getFlowNum(self):
        while True:
            num = Basic.getFlowNum()
            info = Basic.queryOneSellFlowNum(num)
            if info == []:
                return num

    def pay(self):
        '''前台:结算'''
        if self.car.empty():
            print("购物车是空的.")
            return
        all_money = self.car.getMonery()
        pay_money = float(input("请支付{}元:".format(all_money)).strip())
        if pay_money < all_money:
            print("支付失败.")
        else:
            print("支付成功,找零{}元. ".format(pay_money - all_money))
            shop_list = self.car.getlist()
            for com, com_cnt in shop_list:
                #删除库存数量
                Basic.delCommodityCnt(com.getNo(), com_cnt)
                #添加购买信息
                num = self.getFlowNum()
                Basic.addOneSell(self.admin.getNo(), com.getNo(), num, com_cnt,
                                 com.getPrice() * com_cnt)
            print("您已经成功购买以下商品,支付{}元 ,找零{}元 .".format(pay_money,
                                                      pay_money - all_money))
            self.car.printList()
            self.car.clear()

    def show_gui(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("前台界面")
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
            cash_num = username_entry.get().strip()
            cash = Basic.queryOneCashier(cash_num)
            if not cash:
                messagebox.showerror("错误", "不存在该编号")
                return

            self.admin = Cashier(cash)
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
        ttk.Button(button_frame, text="购买功能",
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

    def purchase_gui(self):
        shopping_window = tk.Toplevel(self.window)
        shopping_window.title("购物功能")
        shopping_window.geometry("600x400")

        # 创建购物车显示区域
        cart_frame = ttk.LabelFrame(shopping_window, text="购物车", padding="10")
        cart_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # 创建购物车表格
        cart_table = ttk.Treeview(cart_frame,
                                  columns=("商品编号", "商品名称", "数量", "单价", "小计"),
                                  show="headings")
        for col in cart_table["columns"]:
            cart_table.heading(col, text=col)
        cart_table.pack(fill="both", expand=True)

        # 创建操作按钮
        button_frame = ttk.Frame(shopping_window)
        button_frame.pack(fill="x", padx=10, pady=5)

        ttk.Button(button_frame,
                   text="添加商品",
                   command=lambda: self.add_to_cart_gui(cart_table)).pack(
                       side="left", padx=5)
        ttk.Button(button_frame,
                   text="删除商品",
                   command=lambda: self.remove_from_cart_gui(cart_table)).pack(
                       side="left", padx=5)
        ttk.Button(button_frame,
                   text="清空购物车",
                   command=lambda: self.clear_cart_gui(cart_table)).pack(
                       side="left", padx=5)
        ttk.Button(button_frame,
                   text="结算",
                   command=lambda: self.pay_gui(cart_table)).pack(side="left",
                                                                  padx=5)

    def add_to_cart_gui(self, cart_table):
        com_num = simpledialog.askstring("添加商品", "请输入商品编号:")
        if not com_num:
            return

        com_info = Basic.queryOneCommodity(com_num)
        if not com_info:
            messagebox.showerror("错误", "商品不存在")
            return

        com = Commodity(com_info)
        com_cnt = simpledialog.askinteger("添加商品", "请输入商品数量:")
        if not com_cnt or com_cnt <= 0:
            messagebox.showerror("错误", "购买数量必须大于0")
            return

        if com_cnt > com.getQuantiy():
            messagebox.showerror("错误", "商品库存不足")
            return

        self.car.addCommodity(com, com_cnt)
        self.update_cart_table(cart_table)
        messagebox.showinfo("成功", "添加进入购物车成功")

    def remove_from_cart_gui(self, cart_table):
        selected_item = cart_table.selection()
        if not selected_item:
            messagebox.showwarning("警告", "请先选择要删除的商品")
            return

        item = cart_table.item(selected_item[0])
        com_num = item["values"][0]
        current_cnt = self.car.getCommodityCnt(com_num)

        del_cnt = simpledialog.askinteger("删除商品",
                                          f"当前数量为{current_cnt}，请输入要删除的数量:")
        if not del_cnt:
            return

        self.car.delCommodity(com_num, min(del_cnt, current_cnt))
        self.update_cart_table(cart_table)

    def clear_cart_gui(self, cart_table):
        if messagebox.askyesno("确认", "确定要清空购物车吗？"):
            self.car.clear()
            self.update_cart_table(cart_table)

    def pay_gui(self, cart_table):
        if self.car.empty():
            messagebox.showwarning("警告", "购物车是空的")
            return

        total = self.car.getMonery()
        pay_amount = simpledialog.askfloat("支付", f"请支付{total}元:")

        if not pay_amount or pay_amount < total:
            messagebox.showerror("错误", "支付失败")
            return

        # 处理支付
        shop_list = self.car.getlist()
        for com, com_cnt in shop_list:
            Basic.delCommodityCnt(com.getNo(), com_cnt)
            num = self.getFlowNum()
            Basic.addOneSell(self.admin.getNo(), com.getNo(), num, com_cnt,
                             com.getPrice() * com_cnt)

        messagebox.showinfo("成功", f"支付成功，找零{pay_amount - total}元")
        self.car.clear()
        self.update_cart_table(cart_table)

    def update_cart_table(self, cart_table):
        # 清空表格
        for item in cart_table.get_children():
            cart_table.delete(item)

        # 更新数据
        for com, cnt in self.car.getlist():
            subtotal = com.getPrice() * cnt
            cart_table.insert("",
                              "end",
                              values=(com.getNo(), com.getName(), cnt,
                                      com.getPrice(), subtotal))
