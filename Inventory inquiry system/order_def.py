from sqlite3 import Cursor
from pymysql import Connection
import datetime
import os
import json
class Order_def:

    def __init__(self,path):
        import subprocess
        # 获取数据
        with open(path) as f:
            config = json.load(f)
        # 获取当前日期对象
        self.today = datetime.date.today()
        # 获取和数据库连接对象
        self.conn = Connection(
            host='localhost',
            port=3306,
            user=config['db_username'],
            password=config['db_password'])
        self.cursor = self.conn.cursor()  # 获取游标对象
        self.conn.select_db(config["db_name"])  # use

        # 每个月一次自动数据备份
        def copy_of_database():
            # 定义数据库参数
            db_host = 'localhost'
            self.db_user = config['db_username']
            self.db_password = config['db_password']
            self.db_name = config["db_name"]

            # 获取要备份数据的日期
            if self.today.day >= 25:
                last_month = datetime.date(
                    self.today.year, self.today.month, 25)
            else:
                if self.today.month != 1:
                    last_month = datetime.date(
                        self.today.year, self.today.month - 1, 25)
                else:
                    last_month = datetime.date(self.today.year - 1, 12, 25)

            # 构建备份文件名
            backup_file = f'数据备份/{last_month.strftime("%Y%m%d")}_数据备份.sql'
            self.txt_file = f'操作记录/{last_month.strftime("%Y%m%d")}_操作记录.txt'
            # 获取当前文件夹下的文件列表
            existing_files_sql = os.listdir('数据备份')
            existing_files_txt = os.listdir('操作记录')
            # 检查是否已存在该日期的备份文件
            if not os.path.exists(backup_file):
                # 构建备份命令
                try:
                    backup_command = f'mysqldump -h {db_host} -u {self.db_user} -p{self.db_password} {self.db_name} > {backup_file}'
                    # 执行备份命令
                    subprocess.run(backup_command, shell=True)
                except Exception as e:
                    print(e)
            # 判断文件数量
            if len(existing_files_sql) > 5:  # 只保存5份备份
                # 获取最早的一个备份文件
                earliest_file_sql = sorted(existing_files_sql)[0]
                # 删除最早的备份文件
                os.remove(os.path.join('数据备份', earliest_file_sql))
            if len(existing_files_txt) > 5:
                # 获取最早的一个备份文件
                earliest_file_txt = sorted(existing_files_txt)[0]
                # 删除最早的备份文件
                os.remove(os.path.join('操作记录', earliest_file_txt))

        copy_of_database()

    # 对日期处理,如果不填默认为今天,如果不填年自动补齐
    def optimize_date(self, date):
        if date == '':
            date = str(self.today)
        else:
            i = len(date.split('-'))
            if i == 2:
                date = str(self.today.year) + "-" + date
        return date
    # =====================================================

    #添加供应商名称
    def add_supplier(self, sname):
        try:
            self.cursor.execute(
                "insert into supplier(sname) values(%s);", (sname,))
            self.conn.commit()
            #记录操作
            with open(self.txt_file, 'a', encoding='UTF-8') as f:
                f.write(f"record.add_supplier('{sname}')\n")
            return True
        except Exception as e:
            print(e)
            return False

    #添加采购订单
    def add_PO(self, sname: str, gname: str, qty: str, date: str, p_price: str):
        #对日前处理
        date = self.optimize_date(date)
        #数量分为件数和重量两个纬度
        qty_list = qty.strip().split('-')
        if len(qty_list) != 2:
            return 0
        qty_num = qty_list[0]
        qty_weight = qty_list[1]
        try:
            #添加采购记录
            self.cursor.execute("insert into PO(sname,gname,p_price,p_qty_num,p_qty_weight,p_date) values(%s,%s,%s,%s,%s,%s);",
                                (sname, gname, p_price, qty_num, qty_weight, date))
            #获取当前库存的该商品价格和剩余重量
            self.cursor.execute(
                "select inv_price,inv_qty_weight FROM goods where gname=%s", (gname,))
            tuple_inv_price = self.cursor.fetchall()
            inv_price = float(tuple_inv_price[0][0])  # 价格
            inv_qty_weight = float(tuple_inv_price[0][1])
            #计算单价
            total = inv_price * inv_qty_weight + \
                float(qty_weight) * float(p_price)
            out_put = total / (inv_qty_weight + float(qty_weight))
            #保留两位小数
            out_put = round(out_put, 2)
            #更改该商品库存重量,件数,和单价
            self.cursor.execute(
                "update goods set inv_qty_num = inv_qty_num+%s,inv_qty_weight = inv_qty_weight+%s,inv_price=%s where gname=%s", (qty_num, qty_weight, out_put, gname))
            self.conn.commit()
            #记录操作
            with open(self.txt_file, 'a', encoding='UTF-8') as f:
                f.write(
                    f"record.add_PO('{sname}','{gname}','{qty}','{date}','{p_price}')\n")
            return 1
        except Exception as e:
            error_message = str(e).lower()
            #如果因为外键约束问题
            if "foreign key constraint" in error_message:
                #因为没有gname则返回2
                if "gname" in error_message:
                    return 2
                #因为没有sname则返回3
                elif "sname" in error_message:
                    return 3
                else:
                    print(e)
                    return 0
            else:
                print(e)
                return 0

    #添加销售订单
    def add_GO(self, gname, cname, qty, date, price: str):
        #对日期处理
        date = self.optimize_date(date)
        try:
            #如果输入了价格则修改默认价格,并直接吧price作为售价
            if price.strip():
                is_true = self.update_price(cname, gname, price)
                if not is_true:
                    return False
                cg_price = price
            else:#如果没有输入则获取售价
                self.cursor.execute(
                        "select cg_price FROM cg_name_price where gname=%s and cname= %s ", (gname, cname))
                output2 = self.cursor.fetchall()
                cg_price = str(output2[0][0])
            
            #数量拆分成重量和
            qty_list = qty.strip().split('-')
            if len(qty_list) != 2:
                return False
            qty_num = qty_list[0]
            qty_weight = qty_list[1]
            #获取成本价格
            self.cursor.execute(
                "select inv_price FROM goods where gname=%s", (gname,))
            output1 = self.cursor.fetchall()
            inv_price = str(output1[0][0])
            #添加销售订单记录
            self.cursor.execute("insert into GO(cname,gname,g_price,inv_price,g_qty_num,g_qty_weight,g_date) values(%s,%s,%s,%s,%s,%s,%s);", (
                cname, gname, cg_price, inv_price, qty_num, qty_weight, date))
            #减去库存数量
            self.cursor.execute(
                "update goods set inv_qty_num=inv_qty_num-%s,inv_qty_weight=inv_qty_weight-%s where gname=%s", (qty_num, qty_weight, gname))
            self.conn.commit()
            #记录操作
            with open(self.txt_file, 'a', encoding='UTF-8') as f:
                f.write(f"record.add_GO('{gname}','{cname}','{qty}','{date}')\n")
            return True
        except Exception as e:
            print(e)
            return False

    def add_goods(self, gname: str):
        #把名称型号,拆分成名称,厚度,宽度
        list_goods = gname.strip().split('-')
        if len(list_goods) != 3:
            return False
        try:
            #新建商品信息
            self.cursor.execute("insert into goods(gname,gtype,ply,width,inv_price,inv_qty_num, inv_qty_weight) values(%s,%s,%s,%s,0,0,0);", (
                gname, list_goods[0], list_goods[1], list_goods[2]))
            self.conn.commit()
            #记录操作
            with open(self.txt_file, 'a', encoding='UTF-8') as f:
                f.write(f"record.add_goods('{gname}')\n")
            return True
        except Exception as e:
            print(e)
            return False

    #修改商品和客户出售价格的对应关系
    def update_price(self, cname, gname, price):
        try:
            #进行售价数据更新
            self.cursor.execute(
                "update cg_name_price set cg_price=%s where cname=%s and gname=%s;", (price, cname, gname))
            self.conn.commit()
            #如果有修改成功则记录并结束
            if self.cursor.rowcount > 0:
                with open(self.txt_file, 'a', encoding='UTF-8') as f:
                    f.write(f"record.update_price('{cname}','{gname}','{price}')\n")
                return True
            else:
            #如果没有修改成功则新建对应关系
                self.cursor.execute(
                    "insert into cg_name_price (cname, gname, cg_price) values (%s, %s, %s);", (cname, gname, price))
                self.conn.commit()
                #记录操作
                with open(self.txt_file, 'a', encoding='UTF-8') as f:
                    f.write(f"record.update_price('{cname}','{gname}','{price}')\n")
                return True
        except Exception as e:
            print(e)
            return False

    #运行sql代码
    def run_SQL_code(self, sql):
        try:
            #执行sql语句
            self.cursor.execute(sql)
            #记录操作
            with open(self.txt_file, 'a', encoding='UTF-8') as f:
                f.write(f"record.run_SQL_code('{sql}')\n")
            return True
        except Exception as e:
            print(e)
            return False

    #供应商提示词
    def get_supplier_callword(self, word=""):
        try:
            sql = "SELECT sname FROM supplier"
            parameters = []

            if word.strip():
                sql += " WHERE sname LIKE %s"
                parameters.append(word + '%')

            self.cursor.execute(sql, parameters)
            supplier_names = self.cursor.fetchall()
            return [name[0] for name in supplier_names]

        except Exception as e:
            print(e)
            raise []  # re-raise the exception after printing

    #商品种类提示词
    def get_goods_type_callword(self, word=""):
        try:
            sql = "SELECT DISTINCT gtype FROM goods"
            parameters = []

            if word.strip():
                sql += " WHERE gtype LIKE %s"
                parameters.append(word + '%')

            self.cursor.execute(sql, parameters)
            goods_names = self.cursor.fetchall()
            return [name[0] for name in goods_names]

        except Exception as e:
            print(e)
            raise e  # re-raise the exception after printing

    #型号名称提示词
    def get_goods_gname_callword(self, word=""):
        try:
            sql = "SELECT gname FROM goods"
            parameters = []

            if word.strip():
                sql += " WHERE gname LIKE %s"
                parameters.append(word + '%')

            self.cursor.execute(sql, parameters)
            goods_names = self.cursor.fetchall()
            return [name[0] for name in goods_names]

        except Exception as e:
            print(e)
            raise e  # re-raise the exception after printing

    #客户名称提示词
    def get_customer_callword(self, word=""):
        try:
            sql = "SELECT DISTINCT cname FROM cg_name_price"
            parameters = []

            if word.strip():
                sql += " WHERE cname LIKE %s"
                parameters.append(word + '%')

            self.cursor.execute(sql, parameters)
            customer_names = self.cursor.fetchall()
            return [name[0] for name in customer_names]

        except Exception as e:
            print(e)
            return []  # re-raise the exception after printing

    #搜索采购订单
    def found_PO(self, gname, sname, b__time, e__time):
        try:
            query = "SELECT sname, gname, p_price, p_qty_num,p_qty_weight, p_date FROM po WHERE 1=1"
            parameters = []

            if gname.strip():
                query += " AND gname = %s"
                parameters.append(gname)

            if b__time.strip():
                query += " AND p_date >= %s"
                parameters.append(b__time)

            if e__time.strip():
                query += " AND p_date <= %s"
                parameters.append(e__time)

            if sname.strip():
                query += " AND sname = %s"
                parameters.append(sname)

            self.cursor.execute(query, parameters)
            PO = list(self.cursor.fetchall())
            total_list = [0, 0]
            for record in PO:
                total_list[0] += float(record[3])
                total_list[1] += int(record[4])

            total_list = [round(total, 2) for total in total_list]
            PO.append(("总计", "=====", '=====',*total_list,'====='))
            return PO

        except Exception as e:
            print(e)
            raise e

    #搜索商品订单
    def found_GO(self, gtype, cname, b__time, e__time):
        try:
            query = "SELECT cname, gname, g_price, inv_price, g_qty_num, g_qty_weight, g_date, g_price-inv_price as profit FROM go WHERE 1=1"
            parameters = []

            if gtype.strip():
                query += " AND gname = %s"
                parameters.append(gtype+'%')

            if b__time.strip():
                query += " AND g_date >= %s"
                parameters.append(b__time)

            if e__time.strip():
                query += " AND g_date <= %s"
                parameters.append(e__time)

            if cname.strip():
                query += " AND cname = %s"
                parameters.append(cname)

            self.cursor.execute(query, parameters)
            go_records = list(self.cursor.fetchall())

            total_list = [0, 0, 0, 0, 0, 0]
            for record in go_records:
                total_list[0] += float(record[2])
                total_list[1] += float(record[3])
                total_list[2] += int(record[4])
                total_list[3] += int(record[5])
                total_list[5] += float(record[6])

            total_list = [round(total, 2) for total in total_list]
            go_records.append(("总计", "=====", *total_list))

            return go_records

        except Exception as e:
            print(e)
            return []

    #搜索库存
    def found_goods(self, gtype, thickness, width):
        try:
            query = "SELECT gtype, ply, width, inv_price, inv_qty_num, inv_qty_weight FROM goods WHERE 1=1"
            parameters = []

            if gtype.strip():
                query += " AND gtype = %s"
                parameters.append(gtype)

            if thickness.strip():
                query += " AND ply = %s"
                parameters.append(thickness)

            if width.strip():
                query += " AND width = %s"
                parameters.append(width)
            query += " order by inv_qty_num asc"
            self.cursor.execute(query, parameters)
            goods = self.cursor.fetchall()
            return goods

        except Exception as e:
            print(e)
            return []

    #导出Excel
    def make_excel(self, result, export_path: str, columns):
        import pandas as pd
        try:
            # 创建DataFrame
            df = pd.DataFrame(result, columns=columns)
            # 将DataFrame写入Excel文件
            df.to_excel(export_path, index=False)
            return True
        except Exception as e:
            print(e)
            return False

    #备份数据库
    def copy_database(self, path: str):
        import subprocess
        try:
            db_host = 'localhost'
            backup_command = f'mysqldump -h {db_host} -u {self.db_user} -p{self.db_password} {self.db_name} > {path}'
            # 执行备份命令
            subprocess.run(backup_command, shell=True)
            return True
        except Exception as e:
            print(e)
            return False

    #运行sql文件
    def run_SQL_file(self, path):
        try:
            with open(path, 'r', encoding='UTF-8') as f:
                sql = f.read()
            sql_list = sql.split(';')
            sql_list.pop()
            for code in sql_list:
                self.cursor.execute(code)
            self.conn.commit()
            return True
        except Exception as e:
            print(e)
            return False

    #运行操作记录
    def run_txt_file(self, path):
        try:
            self.copy_database('数据备份/1临时备份.sql')
            with open(path, 'r', encoding='UTF-8') as f:
                codes = f.read()
            codes_list=codes.split('\n')
            codes_list.pop()
            record = untry_def(self.db_user, self.db_password, self.db_name)
            for code in codes_list:
                print(code,end='')
                exec(code)
                print('完成')
            os.remove('数据备份/1临时备份.sql')
            return True
        except Exception as e:
            print(e)
            self.run_SQL_file('数据备份/1临时备份.sql')
            os.remove('数据备份/1临时备份.sql')
            return False
        finally:
            if 'record' in locals():
                del record

# ====================================================================


class untry_def:
    def __init__(self, username: str, password: str, database: str):
        self.conn = Connection(
            host='localhost',
            port=3306,
            user=username,
            password=password)
        self.cursor = self.conn.cursor()  # 获取游标对象
        self.conn.select_db(database)  # use

    def add_supplier(self, sname):
        self.cursor.execute(
            "insert into supplier(sname) values(%s);", (sname,))
        self.conn.commit()

    def add_PO(self, sname: str, gname: str, qty: str, date: str, p_price: str):
        # 输入采购订单信息
        qty_list = qty.strip().split('-')
        qty_num = qty_list[0]
        qty_weight = qty_list[1]
        self.cursor.execute("insert into PO(sname,gname,p_price,p_qty_num,p_qty_weight,p_date) values(%s,%s,%s,%s,%s,%s);",
                            (sname, gname, p_price, qty_num, qty_weight, date))
        self.cursor.execute(
            "select inv_price,inv_qty_weight FROM goods where gname=%s", (gname,))
        tuple_inv_price = self.cursor.fetchall()
        inv_price = float(tuple_inv_price[0][0])  # 价格
        inv_qty_weight = float(tuple_inv_price[0][1])
        total = inv_price * inv_qty_weight + float(qty_weight) * float(p_price)
        out_put = total / (inv_qty_weight + float(qty_weight))
        out_put = round(out_put, 2)
        self.cursor.execute("update goods set inv_qty_num = inv_qty_num+%s,inv_qty_weight = inv_qty_weight+%s,inv_price=%s where gname=%s",
                            (qty_num, qty_weight, out_put, gname))
        self.conn.commit()

    def add_GO(self, gname, cname, qty, date):
        qty_list = qty.strip().split('-')
        qty_num = qty_list[0]
        qty_weight = qty_list[1]

        self.cursor.execute(
            "select inv_price FROM goods where gname=%s", (gname,))
        output1 = self.cursor.fetchall()
        inv_price = str(output1[0][0])
        self.cursor.execute(
            "select cg_price FROM cg_name_price where gname=%s and cname= %s ", (gname, cname))
        # print
        output2 = self.cursor.fetchall()
        cg_price = str(output2[0][0])
        self.cursor.execute("insert into GO(cname,gname,g_price,inv_price,g_qty_num,g_qty_weight,g_date) values(%s,%s,%s,%s,%s,%s,%s);", (
            cname, gname, cg_price, inv_price, qty_num, qty_weight, date))
        self.cursor.execute(
            "update goods set inv_qty_num=inv_qty_num-%s,inv_qty_weight=inv_qty_weight-%s where gname=%s", (qty_num, qty_weight, gname))
        self.conn.commit()

    def add_goods(self, gname: str):
        list_goods = gname.strip().split('-')
        self.cursor.execute("insert into goods(gname,gtype,ply,width,inv_price,inv_qty_num, inv_qty_weight) values(%s,%s,%s,%s,0,0,0);", (
            gname, list_goods[0], list_goods[1], list_goods[2]))
        self.conn.commit()

    def update_price(self, cname, gname, price):

        self.cursor.execute(
            "update cg_name_price set cg_price=%s where cname=%s and gname=%s;", (price, cname, gname))
        self.conn.commit()
        if self.cursor.rowcount == 0:
            self.cursor.execute(
                "insert into cg_name_price (cname, gname, cg_price) values (%s, %s, %s);", (cname, gname, price))
            self.conn.commit()

    def run_SQL_code(self, sql):
        self.cursor.execute(sql)

if __name__=="__main__":
    od = Order_def('配置文件\数据库账号和密码.JSON')
    od.run_txt_file('操作记录/20230625_操作记录.txt')
    