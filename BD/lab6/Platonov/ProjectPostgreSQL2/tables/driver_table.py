from lib.dbtable import *


class DriveTable(DbTable):
    def table_name(self):
        return self.dbconn.prefix + "drivers"

    def columns(self):
        return {
            "id_driver": ["serial", "PRIMARY KEY"],
            "last_name": ["varchar(32)", "NOT NULL"],
            "first_name": ["varchar(32)", "NOT NULL"],
            "second_name": ["varchar(32)"],
            "birthday": ["date", "NOT NULL"],
            "inn": ["numeric", "NOT NULL"],
            "passport_series": ["varchar(12)", "NOT NULL"],
            "passport_num": ["varchar(12)", "NOT NULL"]
        }
# Переписал тип данных id на serial, теперь можно выкинуть sequence 

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


    def add_driver(self, last_name, first_name, second_name, birthday, inn, passport_series, passport_num):
        # Create the sequence if it doesn't exist

        sql = "INSERT INTO " + self.table_name() + " "
        sql += "(" + ", ".join(self.columns().keys()) + ") "
        sql += "VALUES (%(last_name)s, %(first_name)s, %(second_name)s, %(birthday)s, %(inn)s, %(passport_series)s, %(passport_num)s)"
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


    def delete_by_car_id(self, rack_id):
        sql = "DELETE FROM " + self.table_name() + " WHERE id_car = %s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, str(rack_id))
        self.dbconn.conn.commit()
    # Разнес лишие методы из DbTable по файлам, убрал лишние переопределения 