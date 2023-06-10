from lib.dbtable import *


class CarTable(DbTable):
    def table_name(self):
        return self.dbconn.prefix + "cars"

    def columns(self):
        return {"id_car": ["serial", "PRIMARY KEY"],
        # Переписал тип данных id на serial, теперь можно выкинуть sequence 
                "mark": ["varchar(32)", "NOT NULL"],
                "class2": ["varchar(32)", "NOT NULL"],
                "color": ["varchar(32)", "NOT NULL"],
                "gos_number": ["varchar(12)", "NOT NULL"],
                "year": ["numeric", "NOT NULL"],
                "drivers_id": ["integer", f'REFERENCES {self.dbconn.prefix}drivers ON DELETE CASCADE'] # добавил референс к таблице 1 
                "drivers_id": ["integer", f'REFERENCES {self.dbconn.prefix}drivers ON DELETE CASCADE']
                }

    def primary_key(self):
        return ['id_car']

    def delete_car(self, car_id):
        sql = "DELETE FROM " + self.table_name() + " WHERE id_car = %s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, str(car_id))
        self.dbconn.conn.commit()

    def add_car(self, mark, class2, color, gos_number):
        sql = "INSERT INTO " + self.table_name() + " "
        sql += "(" + ", ".join(self.columns().keys()) + ") "
        # sql += "VALUES (" + ", ".join(["%s"] * len(self.columns())) + ")"
        sql += "VALUES (nextval('driver_id_seq'), %(mark)s, %(class2)s, %(color)s, %(gos_number)s, %(year)s, " \
               "%(drivers_id)s, )"
        cur = self.dbconn.conn.cursor()
        print(sql)
        cur.execute(sql, {"mark": mark, "class2": class2, "color": color, "gos_number": gos_number})
        self.dbconn.conn.commit()


def all_by_car_id(self, id_driver):
    sql = "SELECT * FROM " + self.table_name()
    sql += " WHERE drivers_id =%(id)s"
    sql += " ORDER BY " + ", ".join(self.primary_key())
    cur = self.dbconn.conn.cursor()
    cur.execute(sql, {"id": str(id_driver)})
    return cur.fetchall()


    def create(self):
        sql = "CREATE TABLE " + self.table_name() + "("
        arr = [k + " " + " ".join(v) for k, v in self.columns().items()]
        sql += ", ".join(arr + self.table_constraints())
        sql += ")"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        self.dbconn.conn.commit()
        return


    def exists(self, car_id):
        sql = "SELECT * FROM " + self.table_name()
        sql += " WHERE id_car =%(id)s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, {"id": str(car_id)})
        return cur.fetchone()

    def delete_by_id_drivers(self, id):
        sql = "DELETE FROM " + self.table_name() + " WHERE id_driver = %s"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (id,))
        self.dbconn.conn.commit()