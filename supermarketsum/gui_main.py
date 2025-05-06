import tkinter as tk
from tkinter import ttk, messagebox
import pymysql
from basic import Basic
from frontdesk import FrontDesk
from purchasemanage import PurchaseManage
from adminmanage import AdminManage


class SupermarketGUI:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("超市管理系统")
        self.root.geometry("800x600")

        # 设置样式
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TButton",
                             padding=10,
                             font=('微软雅黑', 10),
                             background='#4a90e2',
                             foreground='white')
        self.style.configure("TLabel",
                             padding=6,
                             font=('微软雅黑', 10),
                             background='#f0f0f0')

        # 配置根窗口的网格权重
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # 创建主框架
        main_container = tk.Frame(self.root, bg='#f0f0f0')
        main_container.grid(row=0, column=0, sticky="nsew")

        # 配置主框架的网格权重
        main_container.grid_rowconfigure(0, weight=1)
        main_container.grid_columnconfigure(0, weight=1)

        # 创建内容框架
        content_frame = ttk.Frame(main_container)
        content_frame.grid(row=0, column=0, sticky="nsew")
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)

        # 创建标题
        title_label = ttk.Label(content_frame,
                                text="超市管理系统",
                                font=("微软雅黑", 36))
        title_label.grid(row=0, column=0, pady=40)

        # 创建按钮框架
        button_frame = ttk.Frame(content_frame)
        button_frame.grid(row=1, column=0, pady=20)

        # 创建按钮
        self.create_buttons(button_frame)

        # 连接数据库
        try:
            self.conn = self.link()
            Basic.setConn(self.conn)
        except Exception as e:
            messagebox.showerror("错误", f"数据库连接失败：{str(e)}")
            self.root.destroy()

    def link(self):
        return pymysql.connect(host="127.0.0.1",
                               user="root",
                               password="2540065sga2005",
                               database="supermarket",
                               charset="utf8")

    def create_buttons(self, parent):
        # 售货员界面按钮
        cashier_btn = ttk.Button(parent,
                                 text="售货员界面",
                                 command=self.open_cashier_interface)
        cashier_btn.pack(pady=10, padx=20, fill="x")

        # 进货员界面按钮
        purchaser_btn = ttk.Button(parent,
                                   text="进货员界面",
                                   command=self.open_purchaser_interface)
        purchaser_btn.pack(pady=10, padx=20, fill="x")

        # 管理员界面按钮
        admin_btn = ttk.Button(parent,
                               text="管理员界面",
                               command=self.open_admin_interface)
        admin_btn.pack(pady=10, padx=20, fill="x")

        # 退出按钮
        exit_btn = ttk.Button(parent, text="退出系统", command=self.root.destroy)
        exit_btn.pack(pady=10, padx=20, fill="x")

    def open_cashier_interface(self):
        front_desk = FrontDesk()
        front_desk.show_gui(self.root)

    def open_purchaser_interface(self):
        purchase_manage = PurchaseManage()
        purchase_manage.show_gui(self.root)

    def open_admin_interface(self):
        admin_manage = AdminManage()
        admin_manage.show_gui(self.root)

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    app = SupermarketGUI()
    app.run()
