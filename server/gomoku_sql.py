#encoding=utf-8
import re
import pymysql

class db_process(object):
    def __init__(self, db, host, user, passwd, id_field = "id", default_table = None, charset = "utf8"):
        self.database_name = db
        self.host = host
        self.user = user
        self.passwd = passwd
        self.charset = charset
        self.default_table = default_table
        self.id_field = id_field


    def connect(self):
        try:
            self.db = pymysql.connect(host=self.host,
                                     user=self.user,
                                     passwd=self.passwd,
                                     db=self.database_name,
                                     charset="utf8")
            self.cursor = self.db.cursor()
        except pymysql.Error as e:
            raise e


    def get_pwd_with_id(self, id, field="pwd", table="default"):
        if table == "default":
            table = self.default_table
        command = """select {} from {} where {}={}"""
        self.cursor.execute(command.format(field, table, self.id_field, id))
        result = self.cursor.fetchone()#获取单条
        if result != None:
            return result[0]
        else:
            return "Not Found!"



    def write_data_with_id(self, id, pwd,table=""):
        try:
            command = """INSERT INTO {}(id,pwd)
                        VALUES("{}","{}");""".format(table,id,pwd)
            print(command)
            self.cursor.execute(command)
            self.db.commit()
            return "Reg Success!"
        except:
            return "Reg Failed!"
    
if __name__ == "__main__":
    sql = db_process(db="gomoku",host="127.0.0.1",user="root",passwd="199814",default_table="player_info")
    id = input("输入用户id\n")
    pwd = input("输入用户密码\n")
    sql.connect()
    sql.write_data_with_id(id,pwd,"player_info")
    print(sql.get_pwd_with_id(id))

