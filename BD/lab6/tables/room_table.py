from dbtable import *

class RoomTable(DbTable):
    def table_name(self):
        return self.dbconn.prefix + "Room"

    def columns(self):
        return {
        "id":["serial","PRIMARY KEY"],
        "name": ["character varying(50)", "NOT NULL"],
        "space": ["numeric(7,2)", "NOT NULL"],
        "space_left":["numeric(7,2)", "NOT NULL"],
        "min_humidity":["numeric(8,2)","NOT NULL"],
        "max_humidity":["numeric(8,2)" ,"NOT NULL"],
        "min_temp": ["numeric(5,2)", "NOT NULL"],
        "max_temp":["numeric(5,2)","NOT NULL"]}
    def table_constraints (self):
        return ([
        "CONSTRAINT uni_room_name UNIQUE (name)",
	   "CONSTRAINT positive_volume_left_room CHECK(space_left >0)",
	   "CONSTRAINT positive_volume_room CHECK(space >0)",
	   "CONSTRAINT volume_left_le_volume CHECK(space_left <= space)",
	   "CONSTRAINT hu_max_in_interval CHECK (max_humidity <= 100 and max_humidity >= 0)",
	   "CONSTRAINT hu_min_in_interval CHECK (min_humidity <= 100 and min_humidity >= 0)"
       ])



    def delete_room(self):
        id_ = int(input("Введите номер комнаты, которую хотите удалить: ").strip())
        sql = "DELETE FROM " + self.table_name()
        sql += f" WHERE id = {str(id_)}"
        print(sql)
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        self.dbconn.conn.commit()
        self.show_rooms()

    def show_rooms(self):
        menu = """Просмотр списка комнат!
№\tИмя\tОбъем\t"""
        print(menu)
        lst = self.all()
        for i in lst:
            print(str(i[0]) + "\t" + str(i[1]) + "\t" + str(i[2]))
        menu = """Дальнейшие операции:
    0 - возврат в главное меню;
    3 - добавление новой комнаты;
    4 - удаление комнаты;
    5 - просмотр стеллажей комнаты;
    9 - выход."""
        print(menu)
        return
	

