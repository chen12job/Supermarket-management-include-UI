#Py文件分下面几个
核心文件：
1.gui_main.py 主程序入口 创建主窗口界面 提供三个主要功能入口：售货员、进货员、管理员界面 负责数据库连接初始化 
2.basic.py 数据库操作的基础类 提供所有数据库CRUD操作 包含连接管理、查询执行等功能 作为其他类的数据访问层 
3.frontdesk.py 售货员界面实现 包含购物车功能 实现商品查询、购买等功能 处理销售交易逻辑
4.purchasemanage.py 进货员界面实现 处理商品入库 管理进货记录 查看库存信息 
5.adminmanage.py 管理员界面实现 管理员工信息 管理商品信息 查看销售统计
实体类文件：
1.commodity.py 商品实体类 包含商品属性：编号、名称、类型、规格等 提供商品信息展示功能
2.cashier.py 售货员实体类 包含售货员属性：编号、姓名、密码等 管理售货员信息 
3.purchaser.py 进货员实体类 包含进货员属性：编号、姓名、性别等 管理进货员信息 
4.admin.py 管理员实体类 包含管理员属性：编号、密码等 管理系统权限 
5.sell.py 销售记录实体类 记录销售交易信息 包含商品编号、销售数量、时间等

注：该代码是sql课程设计，使用python3.7编写前台和后台与数据库交互的部分（from WTU 软件工程专业 23级CTJ） 其中使用pymysql库进行与数据库的交互.

**运行程序时，只需将这些py放在放在同一目录，只需运行gui_main.py文件,并且需要将mysql 中的root用户，密码改为自己的
