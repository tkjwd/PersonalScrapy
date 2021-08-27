# import MySQLdb
# import MySQLdb.cursors
import pymysql
import pymysql.cursors
import traceback,re


class MysqlHelp(object):
    def __init__(self, host=None, port=None, user=None, pwd=None, db=None, is_dict=None):
        # self.host = "192.168.31.15"
        # self.user = "root"
        # self.passwd = "abc123"
        # self.db = db

        self.host = host
        self.port = port
        self.user = user
        self.pwd = pwd
        self.db = db
        self.is_dict = is_dict

        if is_dict:
            self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.pwd,
                                        database=self.db,
                                        charset='utf8',
                                        cursorclass=pymysql.cursors.DictCursor)
        else:
            self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user, password=self.pwd,
                                        database=self.db,
                                        charset='utf8')
        self.cursor = self.conn.cursor()

    def exe_sql(self, sql, params=None):
        try:
            res = self.cursor.execute(sql, params) if params else self.cursor.execute(sql)
        except Exception as e:
            print(e)
            print(traceback.format_exc())
            res = 0
            pass

        self.conn.commit()
        if sql and (re.search('select|show', sql, re.I)):
            return self.cursor.fetchall()
        # print('执行成功')

        return 1 if res else 0

    def Bulk_insert(self, text_list, sql, num=5000, reset_sql_ending=None):
        '''
        批量插入方法，传入列表，多值时列表里层放的是元祖，元祖里层可以是任何值，单值list则里层不考虑类型
        单值时传入空类型必须是空字符串格式,无论多值还是单值，datetime类型必须为字符串形式

        :reset_sql_ending:更新插入语句，结尾用
        :param text_list:
        :param sql:
        :param num:
        :return:
        '''

        reset_sql = sql

        k = 0
        text = ''
        if not isinstance(text_list[0], tuple):
            for i in range(int(len(text_list) // num)):
                for j in range(i * num, (i + 1) * num):
                    if text_list[j] != '':
                        value = "('%s')," % text_list[j]
                        reset_sql += str(value)
                reset_sql = reset_sql.rstrip(',') + reset_sql_ending if reset_sql_ending else reset_sql.rstrip(',')
                self._exe(reset_sql)  # 执行批量插入操作
                reset_sql = sql
            for i in range(j + 1, j + (int(len(text_list) % num)) + 1):
                value = "('%s')," % text_list[i]
                reset_sql += str(value)
            reset_sql = reset_sql.rstrip(',') + reset_sql_ending if reset_sql_ending else reset_sql.rstrip(',')
            self._exe(reset_sql)
        else:
            for i in range(int(len(text_list) // num)):
                for j in range(i * num, (i + 1) * num):
                    reset_sql += str(text_list[j]).replace("None", "NULL").replace("''", 'NULL') + ','
                reset_sql = reset_sql.rstrip(',') + reset_sql_ending if reset_sql_ending else reset_sql.rstrip(',')
                self._exe(reset_sql)
                reset_sql = sql
                pass

            for i in range(j + 1, j + int(len(text_list) % num + 1)):
                reset_sql += str(text_list[i]).replace("None", "NULL").replace("''", 'NULL') + ','
            reset_sql = reset_sql.rstrip(',') + reset_sql_ending if reset_sql_ending else reset_sql.rstrip(',')
            if reset_sql != sql:
                self._exe(reset_sql)

# if __name__ == '__main__':
#     My = Mysql_Help('meituan_test', is_dict=True)
#     is_1 = My._exe(None, None)
#     print()
