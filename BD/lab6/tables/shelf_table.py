from dbtable import *

class ShelfTable(DbTable):
    def table_name(self)->str:
        return self.dbconn.prefix + "Shelf"
    def columns(self)->dict:
        return {
        "shelf_id":["serial","PRIMARY KEY"],
        "room_id":["integer",'REFERENCES "C21-703-7".Room ON DELETE CASCADE'],
        "max_spaces":["integer","NOT NULL"],
        "spaces_left":["integer", "NOT NULL"],
        "slot_w":["numeric(7,0)", "NOT NULL"],
        "slot_h":["numeric(7,0)","NOT NULL"],
        "slot_l":["numeric(7,0)", "NOT NULL"],
        "max_weight":["numeric(7,2)", "NOT NULL"],
        "weight_left":["numeric(7,2)", "NOT NULL"]
        }

    def table_constraints(self)->list:
        return[
        "CONSTRAINT positive_size_slot_w_shelf CHECK(slot_w >0)",
        "CONSTRAINT positive_size_slot_h_shelf CHECK(slot_h >0)",
        "CONSTRAINT positive_size_slot_l_shelf CHECK(slot_l >0)",
        "CONSTRAINT positive_weight_shelf CHECK(max_weight >0)",
        "CONSTRAINT positive_weight_left_shelf CHECK(weight_left >0)",
        "CONSTRAINT wight_left_le_weight CHECK(weight_left <= max_weight)"
        ]
    def primary_key(self)->list:
        return ['shelf_id']
        
    def all_by_room_id(self, room_id:int):
        sql = "SELECT * FROM " + self.table_name()
        sql += " WHERE room_id = (%s)"
        sql += " ORDER BY "
        sql += ", ".join(self.primary_key())
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (str(room_id),))
        return cur.fetchall()

    def delete_shelf(self):
        try:
            id_ = int(input("Введите номер полки, которую хотите удалить: ").strip())
        except ValueError as e:
            print("неверно! Введите число!")
            return
        sql = "DELETE FROM " + self.table_name()
        sql += f" WHERE {self.primary_key()[0]} = (%s)"
        print(sql)
        cur = self.dbconn.conn.cursor()
        cur.execute(sql,(str(id_),))
        self.dbconn.conn.commit()


    def __call_creation_wizard(self)->list:
        try:
            rid = int(input("В какую комнату добавить новую полку?: "))
            if rid not in self.create_list_of_ids():
                raise ValueError
        except ValueError as e:
            print("ошибка, введите верное число")
            return []

        try:
            max_spaces = int(input("Введите количество мест на полке: "))
        except ValueError as e:
            print("Введите число, то что ты ввел, редиска, не число")
            return []
        if max_spaces <= 0:
            print("Недопустимое количество мест")
            return []
        spaces_left = max_spaces
        try:
            l,w,h = map(float, input("Введите габариты места на полке, разделяя их пробелом: ").split())
        except ValueError as e:
            print("ты в курсе что такое три числа?")
            return []
        if(l <= 0 or w <= 0 or h <= 0):
            print("Недопустимый габарит")
            return []
        try:
            max_weight = float(input("Введите максимальный нагрузочный вес полки: "))
        except ValueError as e:
            print("Вес - число, а не то что ты ввел")
        if max_weight <= 0:
            print("Недопустимый вес")
            return []
        weight_left = max_weight
        return [rid,max_spaces,spaces_left,w,h,l,max_weight,weight_left]






    def add_shelf_attached_to_room(self)-> None:
        data = self.__call_creation_wizard()
        if data:
            self.insert_one(data)
            print("Полка создана")
            return
        print("Полка не создана, ошибка")
        return


    def del_shelf_by_room(self,room_id:int):
        lst = self.all_by_room_id(room_id)
        for i in lst:
            print(str(i[0]) + "\t" + str(i[1]) + "\t" + str(i[2]))
            self.delete_shelf()
            self.all_by_room_id(room_id)






