from dbtable import *

class ShelfTable(DbTable):
    def table_name(self):
        return self.dbconn.prefix + "Shelf"
    def columns(self):
        return {
        "shelf_id":["integer","PRIMARY KEY"],
        "room_id":["integer",'REFERENCES "C21-703-7"."Room"'],
        "max_spaces":["integer","NOT NULL"],
        "spaces_left":["integer", "NOT NULL"],
        "slot_w":["numeric(7,0)", "NOT NULL"],
        "slot_h":["numeric(7,0)","NOT NULL"],
        "slot_l":["numeric(7,0)", "NOT NULL"],
        "max_weight":["numeric(7,2)", "NOT NULL"],
        "weight_left":["numeric(7,2)", "NOT NULL"]
        }

    def table_constraints(self):
        return
        [
        "CONSTRAINT positive_size_slot_w_shelf CHECK(slot_w >0)",
        "CONSTRAINT positive_size_slot_h_shelf CHECK(slot_h >0)",
        "CONSTRAINT positive_size_slot_l_shelf CHECK(slot_l >0)",
        "CONSTRAINT positive_weight_shelf CHECK(max_weight >0)",
        "CONSTRAINT positive_weight_left_shelf CHECK(weight_left >0)",
        "CONSTRAINT wight_left_le_weight CHECK(weight_left <= max_weight)"]

    def all_by_room_id(self, room_id):
        sql = "SELECT * FROM " + self.table_name()
        sql += " WHERE room_id = %s"
        sql += " ORDER BY shelf_id "
        sql += ", ".join(self.primary_key())
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, str(room_id))
        return cur.fetchall()

    def delete_shelf(self):
        id_ = int(input("Введите номер полки, которую хотите удалить: ").strip())
        sql = "DELETE FROM " + self.table_name()
        sql += f" WHERE id = {str(id_)}"
        print(sql)
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        self.dbconn.conn.commit()


    def __call_creation_wizard(self):
        from room_table import RoomTable as RT
        RT = RT()
        sql = f"SELECT max(id) FROM {RT.table_name()}"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        new_id = cur.fetchone()[0] + 1
        RT.show_rooms()
        rid = int(input("В какую комнату добавить новую полку?: "))
        max_spaces = int(input("Введите количество мест на полке: "))
        if max_spaces <= 0:
            print("Недопустимое количество мест")
            return []
        spaces_left = max_spaces
        l,w,h = map(float, input("Введите габариты места на полке, разделяя их пробелом: ").split())
        if(l <= 0 or w <= 0 or h <= 0):
            print("Недопустимый габарит")
            return []
        max_weight = float(input("Введите максимальный нагрузочный вес полки: "))
        if max_weight <= 0:
            print("Недопустимый вес")
            return []
        weight_left = max_weight
        return [new_id,rid,max_spaces,spaces_left,l,w,h,max_weight,weight_left]
        ## TODO: проверка того что id комнаты валидный






    def add_shelf_attached_to_room(self):
        data = self.__call_creation_wizard()
        if data:
            self.insert_one(data)
            print("Полка создана")
            return
        print("Полка не создана, ошибка")
        return


    def del_shelf_by_room(shelf,room_id):
        lst = self.all_by_room_id(room_id)
        for i in lst:
            print(str(i[0]) + "\t" + str(i[1]) + "\t" + str(i[2]))
            self.delete_shelf()
            self.all_by_room_id(room_id)






