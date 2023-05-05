# Базовые действия с таблицами

from dbconnection import *

class DbTable:
    dbconn = None

    def __init__(self)->None:
        return

    def table_name(self)->str:
        return self.dbconn.prefix + "table"

    def columns(self)->dict:
        return {"test": ["integer", "PRIMARY KEY"]}

    def column_names(self)->list:
        return self.columns().keys()

    def primary_key(self)->list:
        return ['id']

    def column_names_without_id(self)->list:
        res = list(self.columns().keys())
        for col in self.primary_key():
            res.remove(col)
        return res

    def table_constraints(self)->list:
        return []

    def create(self)->None:
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

    def drop(self)->None:
        sql = "DROP TABLE IF EXISTS " + self.table_name()
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        self.dbconn.conn.commit()
        return

    def insert_one(self, vals:list)->None:
        for i in range(0, len(vals)):
            if type(vals[i]) == str:
                vals[i] = "'" + vals[i] + "'"
            else:
                vals[i] = str(vals[i])
        sql = "INSERT INTO " + self.table_name() + "("
        sql += ",".join(self.column_names_without_id()) + ") VALUES("
        sql +=  "(%s)," * (len(vals)-1) + "(%s)" + ")"
        print(sql)
        cur = self.dbconn.conn.cursor()
        #print(sql)
        cur.execute(sql, vals)
        self.dbconn.conn.commit()
        return

    def first(self)->list:
        sql = "SELECT * FROM " + self.table_name()
        sql += " ORDER BY "
        sql += ", ".join(self.primary_key())
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        return cur.fetchone()        

    def last(self)->list:
        sql = "SELECT * FROM " + self.table_name()
        sql += " ORDER BY "
        sql += ", ".join([x + " DESC" for x in self.primary_key()])
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        return cur.fetchone()

    def all(self)->list:
        sql = "SELECT * FROM " + self.table_name()
        sql += " ORDER BY "
        sql += ", ".join(self.primary_key())
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        return cur.fetchall()        
    

