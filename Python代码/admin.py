class Admin:

    def __init__(self, username=None, password=None, info=None):
        """
        Admin构造函数，支持两种初始化方式
        1. 通过username和password初始化
        2. 通过info列表初始化
        """
        if info is not None:
            self.info = info
            self.username = info[0]
            self.password = info[1]
        else:
            self.username = username
            self.password = password
            self.info = [username, password]

    def getNo(self):
        return self.info[0]

    def getPwd(self):
        return self.info[1]

    def get_username(self):
        return self.username

    def verify_login(self):
        """验证管理员登录"""
        try:
            from basic import Basic
            sql = f"SELECT * FROM Admin WHERE admin_no='{self.username}' AND admin_pwd='{self.password}'"
            result = Basic.runQuery(sql)
            return len(result) > 0
        except Exception as e:
            print(f"管理员登录验证错误: {e}")
            return False
