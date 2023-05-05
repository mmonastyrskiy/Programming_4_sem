from dbtable import *

class RoomTable(DbTable):
    def table_name(self) -> str:
        return self.dbconn.prefix + "Room"

    def columns(self)->dict:
        return {
        "id":["serial","PRIMARY KEY"],
        "name": ["character varying(50)", "NOT NULL"],
        "space": ["numeric(7,2)", "NOT NULL"],
        "space_left":["numeric(7,2)", "NOT NULL"],
        "min_humidity":["numeric(8,2)","NOT NULL"],
        "max_humidity":["numeric(8,2)" ,"NOT NULL"],
        "min_temp": ["numeric(5,2)", "NOT NULL"],
        "max_temp":["numeric(5,2)","NOT NULL"]}
    def table_constraints (self)->list:
        return ([
        "CONSTRAINT uni_room_name UNIQUE (name)",
	   "CONSTRAINT positive_volume_left_room CHECK(space_left >0)",
	   "CONSTRAINT positive_volume_room CHECK(space >0)",
	   "CONSTRAINT volume_left_le_volume CHECK(space_left <= space)",
	   "CONSTRAINT hu_max_in_interval CHECK (max_humidity <= 100 and max_humidity >= 0)",
	   "CONSTRAINT hu_min_in_interval CHECK (min_humidity <= 100 and min_humidity >= 0)"
       ])



    def delete_room(self)->None:
        try:
            id_ = int(input("Введите номер комнаты, которую хотите удалить: ").strip())
            print(id_)
        except ValueError as e:
            print("Введите номер по списку, введеное значение - не число")
            return
        sql = "DELETE FROM " + self.table_name()
        sql += f" WHERE id = (%s)"
        #print(sql)
        cur = self.dbconn.conn.cursor()
        id_ = str(id_)
        cur.execute(sql, (id_,))
        self.dbconn.conn.commit()
        self.show_rooms()

    def show_rooms(self)->None:
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

    def __call_creation_wizard(self)->list:
        name = input("Введите название комнаты: ")
        try:
            space = float(input("Введите объем комнаты: "))
        except ValueError as e:
            print("Введено неверное число")
            return []

        try:
            minh = float(input("Введите минимальную влажность"))
            maxh = float(input("Введите максимальную влажность"))
            if not((0<= minh <= 100) and (0 <= maxh <= 100) and minh <= maxh):
                raise ValueError
        except ValueError as e:
            print("Одна или обе из влажностей введена(ы) неверно")
            return []

        try:
            mint = float(input("Введите минимальную температуру"))
            maxt = float(input("Введите максимальную температуру"))
            if not((0<= mint <= 100) and (0 <= maxt <= 100) and mint <= maxt):
                raise ValueError
        except ValueError as e:
            print("Одна или обе из температур введена(ы) неверно")
            return []
        return [name,space,space,minh,maxh,mint,maxt]
        




    def add_rooms(self)-> None:
        data = self.__call_creation_wizard()
        if data:
            self.insert_one(data)
            print("комната создана")
            return
        print("комната не создана, ошибка")
        return

