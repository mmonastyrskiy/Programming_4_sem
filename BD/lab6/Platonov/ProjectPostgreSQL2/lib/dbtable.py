# Базовые действия с таблицами
from dbconnection import *


class DbTable:
    dbconn = None

    def __init__(self):
        return

    def table_name(self):
        return self.dbconn.prefix + "table"

    def columns(self):
        return {"test": ["integer", "PRIMARY KEY"]}

    def column_names(self):
        return (self.columns().keys())

    def primary_key(self):
        return ['id']
# переписал криво написанные методы
    def column_names_without_id(self)->list:
        """
        возвращает список колонок не включая ключ
        """
        res = list(self.columns().keys())
        for col in self.primary_key():
            res.remove(col)
        return res


    def table_constraints(self):
        return []
    # Переписал мето Create убрав сортировку столбцов по алфавиту, из-за нее проблема при вставке новых машин

    def create(self)->None:
        """
        Создать таблицу в БД
        """
        sql = "CREATE TABLE " + self.table_name() + "("
        arr = [k + " " + " ".join(v) for k, v in self.columns().items()]
        #print(arr)
        sql += ", ".join(arr + self.table_constraints())
        sql += ")"
        #print(sql)
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        self.dbconn.conn.commit()
        return

    def drop(self):
        sql = "DROP TABLE IF EXISTS " + self.table_name() + " CASCADE"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        self.dbconn.conn.commit()
        return
    # Переписал метод Insert_one т к он допускал наличие SQLi

    def insert_one(self, vals:list)->None:
        """
        Добавить запись в таблицу
        """
        sql = "INSERT INTO " + self.table_name() + "("
        sql += ",".join(self.column_names_without_id()) + ") VALUES("
        sql +=  "(%s)," * (len(vals)-1) + "(%s)" + ")"
        #print(sql)
        cur = self.dbconn.conn.cursor()
        #print(sql)
        cur.execute(sql, vals)
        self.dbconn.conn.commit()
        return

    def first(self):
        sql = "SELECT * FROM " + self.table_name()
        sql += " ORDER BY "
        sql += ", ".join(self.primary_key())
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        return cur.fetchone()

    def last(self):
        sql = "SELECT * FROM " + self.table_name()
        sql += " ORDER BY "
        sql += ", ".join([x + " DESC" for x in self.primary_key()])
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        return cur.fetchone()

    def all(self):
        sql = "SELECT * FROM " + self.table_name()
        sql += " ORDER BY "
        sql += ", ".join(self.primary_key())
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        return cur.fetchall()



    def create_list_of_ids(self)-> list:
        """
        список айдишников в таблице
        """
        sql = f"SELECT {self.primary_key()[0]} FROM " + self.table_name()
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        ids = [x[0] for x in cur.fetchall()]
        #print(ids)
        return ids


