from dbtable import *
from room_table import RoomTable
import colorama
import pglimits
from colorama import Fore, Back, Style
colorama.init()


class ShelfTable(DbTable):
    def table_name(self)->str:
        """
        Возвращает строку префикс + полка
        """
        return self.dbconn.prefix + "Shelf"
    def columns(self)->dict:
        """
        возвращает колонки + локальные ограничения целостности
        """
        return {
        "shelf_id":["serial","PRIMARY KEY"],
        "room_id":["integer",f'REFERENCES {self.dbconn.prefix}Room ON DELETE CASCADE'],
        "max_spaces":["integer","NOT NULL"],
        "spaces_left":["integer", "NOT NULL"],
        "slot_w":["numeric(7,0)", "NOT NULL"],
        "slot_h":["numeric(7,0)","NOT NULL"],
        "slot_l":["numeric(7,0)", "NOT NULL"],
        "max_weight":["numeric(7,2)", "NOT NULL"],
        "weight_left":["numeric(7,2)", "NOT NULL"]
        }

    def table_constraints(self)->list:
        """
        Возвращает общие ограничения целостности
        """
        return[
        "CONSTRAINT positive_size_slot_w_shelf CHECK(slot_w >0)",
        "CONSTRAINT positive_size_slot_h_shelf CHECK(slot_h >0)",
        "CONSTRAINT positive_size_slot_l_shelf CHECK(slot_l >0)",
        "CONSTRAINT positive_weight_shelf CHECK(max_weight >0)",
        "CONSTRAINT positive_weight_left_shelf CHECK(weight_left >0)",
        "CONSTRAINT wight_left_le_weight CHECK(weight_left <= max_weight)"
        ]
    def primary_key(self)->list:
        """
        Возвращает список ключевых полей
        """
        return ['shelf_id']
        
    def all_by_room_id(self, room_id:int):
        rt = RoomTable()
        """
        Возвращает список полок по айди комнаты
        """
        if room_id not in rt.create_list_of_ids():
            print(Fore.RED +"неверное значение, Выберите существующее" + Style.RESET_ALL)
        sql = "SELECT * FROM " + self.table_name()
        sql += " WHERE room_id = (%s)"
        sql += " ORDER BY "
        sql += ", ".join(self.primary_key())
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (str(room_id),))
        return cur.fetchall()

    def delete_shelf(self):
        """
        Удаление полки
        """
        try:
            id_ = int(input(Fore.YELLOW+"Введите номер полки, которую хотите удалить: "+Style.RESET_ALL).strip())
            if not id_ in self.create_list_of_ids():
                raise ValueError
        except ValueError as e:
            print(Fore.RED+"неверно! Введите число!"+Style.RESET_ALL)
            self.dbconn.logger.warn(Fore.GREEN+str(e)+Style.RESET_ALL)
            return
        sql = "DELETE FROM " + self.table_name()
        sql += f" WHERE {self.primary_key()[0]} = (%s)"
        #print(sql)
        cur = self.dbconn.conn.cursor()
        cur.execute(sql,(str(id_),))
        self.dbconn.conn.commit()


    def __call_creation_wizard(self)->list:
        rid = None
        max_spaces = None
        rt = RoomTable()
        """
        Мастер создания полок
        """
        while not(type(rid) == int and rid in rt.create_list_of_ids() and (0 < rid <= pglimits.PG_INT_MAX)):
            try:
                rid = int(input(Fore.YELLOW+"В какую комнату добавить новую полку? для отмены введите 0: "+Style.RESET_ALL))
                if not rid:
                    return
                if ((rid not in rt.create_list_of_ids()) or not(pglimits.PG_INT_MIN <= rid <= pglimits.PG_INT_MAX)):
                    raise ValueError
            except ValueError as e:
                print(Fore.RED+"ошибка, введите верное число"+Style.RESET_ALL)
                self.dbconn.logger.warn(Fore.GREEN+str(e)+Style.RESET_ALL)
        while not (type(max_spaces) == int and (0 < max_spaces <= pglimits.PG_INT_MAX)):
            try:
                max_spaces = int(input(Fore.YELLOW+"Введите количество мест на полке для отмены введите 0: "+Style.RESET_ALL))
                if not max_spaces:
                    return
                if not(0 < max_spaces <= pglimits.PG_INT_MAX):
                    raise ValueError
            except ValueError as e:
                print(Fore.RED+"Введите число, то что ты ввел, редиска, не число"+Style.RESET_ALL)
                self.dbconn.logger.warn(Fore.GREEN+str(e)+Style.RESET_ALL)
            if max_spaces < 0:
                print(Fore.RED+"Недопустимое количество мест")
                self.dbconn.logger.warn(Fore.GREEN+str("Недопустимое количество мест")+Style.RESET_ALL)
        spaces_left = max_spaces
        while not ((type(l) == float) and ((0<l<=pglimits.NUMERIC7_0_MAX))
            and (type(w) == float) and ((0<w<=pglimits.NUMERIC7_0_MAX))
            and (type(h) == float) and ((0<h<=pglimits.NUMERIC7_0_MAX))):

            try:
                l,w,h = map(float, input(Fore.YELLOW+"Введите габариты места на полке, разделяя их пробелом: "+Style.RESET_ALL).split())
                if((pglimits.NUMERIC7_0_MIN<=l<=pglimits.NUMERIC7_0_MAX) or (pglimits.NUMERIC7_0_MIN<=h<=pglimits.NUMERIC7_0_MAX) or (pglimits.NUMERIC7_0_MIN<= w<=pglimits.NUMERIC7_0_MAX)):
                    raise ValueError
            except ValueError as e:
                print(Fore.RED+"ты в курсе что такое три числа?"+Style.RESET_ALL)
                self.dbconn.logger.warn(Fore.GREEN+str(e)+Style.RESET_ALL)
            if(l <= 0 or w <= 0 or h <= 0):
                print(Fore.RED+"Недопустимый габарит")
        
        while not((type(max_weight)) and (0 < max_weight <= pglimits.NUMERIC7_2_MAX)):
            try:
                max_weight = float(input(Fore.YELLOW+"Введите максимальный нагрузочный вес полки для отмены введите 0: "+Style.RESET_ALL))
                if not max_weight:
                    return
                if not(0 < max_weight <= pglimits.NUMERIC7_2_MAX):
                    raise ValueError
            except ValueError as e:
                print(Fore.RED+"Вес - число, а не то что ты ввел"+Style.RESET_ALL)
                self.dbconn.logger.warn(Fore.GREEN+str(e)+Style.RESET_ALL)
        if max_weight <= 0:
            print(Fore.RED+"Недопустимый вес"+Style.RESET_ALL)
        weight_left = max_weight
        return [rid,max_spaces,spaces_left,w,h,l,max_weight,weight_left]




    def show_shelves(self)->None:
        """
        отобразить полки
        """
        menu = Fore.YELLOW+""" Просмотр списка полок
№\tКомната\tмакс мест\tоставшиеся места\tгабариты места\tвес макс\t вес оставшийся""" + Style.RESET_ALL
        print(menu)
        lst = self.all()
        for i in lst:
            print(str(i[0]) + "\t" + str(i[1]) + "\t" + str(i[2]) + "\t" + str(i[3]) + "\t"
                f"{str(i[4])} x {str(i[5])} x {str(i[6])}" + "\t" + str(i[7]) + "\t" + str(i[8]))


    def add_shelf_attached_to_room(self)-> None:
        """
        обработчик создания полки
        """
        data = self.__call_creation_wizard()
        if type(data) == list:
            self.insert_one(data)
            print(Fore.GREEN + "полка создана"+ Style.RESET_ALL)

    def del_shelf_by_room(self,room_id:int):
        """
        удаление полки
        """
        lst = self.all_by_room_id(room_id)
        for i in lst:
            print(str(i[0]) + "\t" + str(i[1]) + "\t" + str(i[2]))
            self.delete_shelf()
            self.all_by_room_id(room_id)





    def edit_check(self,id_:int, col_2edit: int, new_data:str)-> bool:
        """
        проверка выполнения ограничений целостности при редактировании полки
        """
        if (col_2edit == 0):
            sql = "UPDATE " + self.table_name() + " SET " +self.column_names_without_id()[col_2edit]
            sql += " = (%s) WHERE " + self.primary_key()[0] + " = (%s)"
            cur = self.dbconn.conn.cursor()
            try:
                RT = RoomTable()
                ids = RT.create_list_of_ids()
                if(int(new_data) not in ids):
                    raise ValueError
            except ValueError as e:
                self.dbconn.logger.warn(Fore.GREEN+str(e)+Style.RESET_ALL)
                return False
            cur.execute(sql, [new_data, str(id_)])
            self.dbconn.conn.commit()
            return True
        elif (col_2edit == 1):
            sql = "UPDATE " + self.table_name() + " SET " +self.column_names_without_id()[col_2edit]
            sql += " = (%s) WHERE " + self.primary_key()[0] + " = (%s)"
            cur = self.dbconn.conn.cursor()
            try:
                sql_ = f"SELECT {self.column_names_without_id()[col_2edit+1]} FROM {self.table_name()} WHERE {self.primary_key()[0]} = (%s)"
                cur = self.dbconn.conn.cursor()
                cur.execute(sql_, tuple(str(id_),))
                recived = list(cur.fetchone())[0]

                if not(float(new_data) >= recived):
                    raise ValueError
            except ValueError as e:
                self.dbconn.logger.warn(Fore.GREEN+str(e)+Style.RESET_ALL)
                return False
            cur.execute(sql, [new_data, str(id_)])
            self.dbconn.conn.commit()
            return True
        elif (col_2edit == 3):
            sql = "UPDATE " + self.table_name() + " SET " +self.column_names_without_id()[col_2edit]
            sql += " = (%s) WHERE " + self.primary_key()[0] + " = (%s)"
            cur = self.dbconn.conn.cursor()
            try:
                if (int(new_data) <= 0):
                    raise ValueError
            except ValueError as e:
                self.dbconn.logger.warn(Fore.GREEN+str(e)+Style.RESET_ALL)
                return False
            cur.execute(sql, [new_data, str(id_)])
            self.dbconn.conn.commit()
            return True
        elif (col_2edit == 4):
            sql = "UPDATE " + self.table_name() + " SET " +self.column_names_without_id()[col_2edit]
            sql += " = (%s) WHERE " + self.primary_key()[0] + " = (%s)"
            cur = self.dbconn.conn.cursor()
            try:
                if (int(new_data) <= 0):
                    raise ValueError
            except ValueError as e:
                self.dbconn.logger.warn(Fore.GREEN+str(e)+Style.RESET_ALL)
                return False
            cur.execute(sql, [new_data, str(id_)])
            self.dbconn.conn.commit()
            return True
        elif (col_2edit == 5):
            sql = "UPDATE " + self.table_name() + " SET " +self.column_names_without_id()[col_2edit]
            sql += " = (%s) WHERE " + self.primary_key()[0] + " = (%s)"
            cur = self.dbconn.conn.cursor()
            try:
                if (int(new_data) <= 0):
                    raise ValueError
            except ValueError as e:
                self.dbconn.logger.warn(Fore.GREEN+str(e)+Style.RESET_ALL)
                return False
            cur.execute(sql, [new_data, str(id_)])
            self.dbconn.conn.commit()
            return True
        elif (col_2edit == 6):
            sql = "UPDATE " + self.table_name() + " SET " +self.column_names_without_id()[col_2edit]
            sql += " = (%s) WHERE " + self.primary_key()[0] + " = (%s)"
            cur = self.dbconn.conn.cursor()
            try:
                sql_ = f"SELECT {self.column_names_without_id()[col_2edit+1]} FROM {self.table_name()} WHERE {self.primary_key()[0]} = (%s)"
                cur = self.dbconn.conn.cursor()
                cur.execute(sql_, (str(id_),))
                recived = list(cur.fetchone())[0]

                if not(float(new_data) >= recived):
                    raise ValueError
            except ValueError as e:
                self.dbconn.logger.warn(Fore.GREEN+str(e)+Style.RESET_ALL)
                return False
            cur.execute(sql, [new_data, str(id_)])
            self.dbconn.conn.commit()
            return True




    def edit_shelf(self):
        """
        редактор полок
        """
        inp = None
        col_2edit = None

        self.show_shelves()
        while not (inp in self.create_list_of_ids()):
            try:
                inp = int(input(Fore.YELLOW + "Выберите полку которую хотите изменить для отмены введите 0: " + Style.RESET_ALL))
                if not inp:
                    return
                if inp not in self.create_list_of_ids():
                    raise ValueError
            except ValueError as e:
                print(Fore.RED+ "Введите правильное число" + Style.RESET_ALL)
                self.dbconn.logger.warn(Fore.GREEN+str(e)+Style.RESET_ALL)

        sql = f"SELECT * FROM {self.table_name()} WHERE {self.primary_key()[0]} = (%s)"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (str(inp),))
        recived = list(cur.fetchone())[1:]
        cols = self.column_names_without_id()
        data = list(zip(cols,recived))
        for col in enumerate(data):
            print(col[0],col[1], sep = "\t")
        while not(type(col_2edit) == int and (0 <= col_2edit < len(data))):
            try:
                col_2edit = int(input(Fore.YELLOW + "Введите номер поля, который хотите изменить: для отмены введите -1 " + Style.RESET_ALL))
                if(col_2edit == -1):
                    return
                if not(0 <= col_2edit < len(data)):
                    raise ValueError
            except ValueError as e:
                self.dbconn.logger.warn(Fore.GREEN+str(e)+Style.RESET_ALL)
                print(Fore.RED + "Введено неверное число"+Style.RESET_ALL)
        new_data = input(Fore.YELLOW+"Введите новое значение поля: "+Style.RESET_ALL)
        if self.edit_check(inp,col_2edit,new_data):
            print(Fore.GREEN+"Изменения применены"+Style.RESET_ALL)
            return
        print(Fore.RED+"Во внесении изменений отказно, неверное новое значение"+Style.RESET_ALL)
        return




