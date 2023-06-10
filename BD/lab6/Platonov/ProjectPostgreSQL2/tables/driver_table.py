from lib.dbtable import *


class DriveTable(DbTable):
    def table_name(self):
        return self.dbconn.prefix + "drivers"

    def columns(self):
        return {
            "id_driver": ["integer", "NOT NULL", "PRIMARY KEY"],
            "last_name": ["varchar(32)", "NOT NULL"],
            "first_name": ["varchar(32)", "NOT NULL"],
            "second_name": ["varchar(32)"],
            "birthday": ["date", "NOT NULL"],
            "inn": ["numeric", "NOT NULL"],
            "passport_series": ["varchar(12)", "NOT NULL"],
            "passport_num": ["varchar(12)", "NOT NULL"]
        }


    def primary_key(self):
        return ['id_driver']

    def find_by_position(self, num):
        sql = "SELECT * FROM " + self.table_name()
        sql += " ORDER BY "
        sql += ", ".join(self.primary_key())
        sql += " LIMIT 1 OFFSET %(offset)s"
        #print(sql)
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, {"offset": int(num) - 1})
        return cur.fetchone()

    def delete_by_id_drivers(self, name):
        sql = "DELETE FROM " + self.table_name()
        sql += f" WHERE id_driver =%(off)s"
        print(sql)
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, {"off": name})
        self.dbconn.conn.commit()

    def sequence(self):
        sql = "CREATE SEQUENCE IF NOT EXISTS drivers_id_seq"
        return sql

    def add_driver(self, last_name, first_name, second_name, birthday, inn, passport_series, passport_num):
        # Create the sequence if it doesn't exist
        cur = self.dbconn.conn.cursor()
        cur.execute(self.sequence())

        sql = "INSERT INTO " + self.table_name() + " "
        sql += "(" + ", ".join(self.columns().keys()) + ") "
        sql += "VALUES (nextval('drivers_id_seq'), %(last_name)s, %(first_name)s, %(second_name)s, %(birthday)s, %(inn)s, %(passport_series)s, %(passport_num)s)"
        cur.execute(sql, {
            "last_name": last_name,
            "first_name": first_name,
            "second_name": second_name,
            "birthday": birthday,
            "inn": inn,
            "passport_series": passport_series,
            "passport_num": passport_num,
        })
        self.dbconn.conn.commit()

    def create(self):
        sql = "CREATE TABLE " + self.table_name() + "("
        arr = [k + " " + " ".join(v) for k, v in self.columns().items()]
        sql += ", ".join(arr + self.table_constraints())
        sql += ")"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        self.dbconn.conn.commit()
        return
