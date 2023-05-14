from dbtable import *
import colorama
import pglimits
from colorama import Fore, Back, Style
from station_table import StationsTable
colorama.init()


class SheduleTable(DbTable):
    def table_name(self)->str:
        """
        Возвращает строку префикс + полка
        """
        return self.dbconn.prefix + "schedule"
    def columns(self)->dict:
        """
        возвращает колонки + локальные ограничения целостности
        """
        return {"id":["serial"],
        "route_id":["integer"],
    "station_id": ["integer","NOT NULL",f"REFERENCES {self.dbconn.prefix}stations (id) ON DELETE CASCADE"],
    '"time"':["time"],
    "track":["integer","NOT NULL"]
    }


    def create_list_of_routes(self)-> list:
        """
        список айдишников в таблице
        """
        sql = f"SELECT route_id FROM " + self.table_name()
        cur = self.dbconn.conn.cursor()
        cur.execute(sql)
        ids = [x[0] for x in cur.fetchall()]
        #print(ids)
        return ids

    def table_constraints(self)->list:
        """
        Возвращает общие ограничения целостности
        """
        return["UNIQUE (station_id, route_id)"]

    def delete_station(self):
        """
        Удаление полки
        """
        try:
            id_ = int(input(Fore.YELLOW+"Введите номер остановки, которую хотите удалить: "+Style.RESET_ALL).strip())
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
    def time_validator(self,x:str)-> bool:
        x = x.strip().split(":")
        try:
            h,m,s = x
            if (not(0<=int(h)<=23) and not(0<=int(m)<=59) and not(0<=int(s)<=59)):
                return False
            return True
        except ValueError as e:
            print(Fore.RED+"неверно! Введите время в установленном формате (HH:MM:SS)!"+Style.RESET_ALL)
            self.dbconn.logger.warn(Fore.GREEN+str(e)+Style.RESET_ALL)

    def __call_creation_wizard(self)->list:
        rid =sid=None
        track = None
        x = ""
        st = StationsTable()
        """
        Мастер создания полок
        """
    
        while not(type(sid) == int and sid in st.create_list_of_ids() and (0 < sid <= pglimits.PG_INT_MAX)):
            try:
                sid = int(input(Fore.YELLOW+"Какую станцию добавить? для отмены введите 0: "+Style.RESET_ALL))
                if not sid:
                    return
                if ((sid not in st.create_list_of_ids()) or not(pglimits.PG_INT_MIN <= sid <= pglimits.PG_INT_MAX)):
                    raise ValueError
            except ValueError as e:
                print(Fore.RED+"ошибка, введите верное число"+Style.RESET_ALL)
                self.dbconn.logger.warn(Fore.GREEN+str(e)+Style.RESET_ALL)

        while not(type(rid) == int and rid in self.create_list_of_routes() and (0 < rid <= pglimits.PG_INT_MAX)):
            try:
                rid = int(input(Fore.YELLOW+"К какому маршруту добавить станцию? для отмены введите 0: "+Style.RESET_ALL))
                if not rid:
                    return
                if ((rid not in self.create_list_of_routes()) or not(pglimits.PG_INT_MIN <= rid <= pglimits.PG_INT_MAX)):
                    raise ValueError
            except ValueError as e:
                print(Fore.RED+"ошибка, введите верное число"+Style.RESET_ALL)
                self.dbconn.logger.warn(Fore.GREEN+str(e)+Style.RESET_ALL)


        while not((type(track)==int) and (0 < track <= pglimits.PG_INT_MAX)):
            try:
                track = int(input(Fore.YELLOW+"Введите путь прибытия для отмены введите 0: "+Style.RESET_ALL))
                if not track:
                    return
                if not(0 < track <= pglimits.PG_INT_MAX):
                    raise ValueError
            except ValueError as e:
                print(Fore.RED+"путь - число, а не то что ты ввел"+Style.RESET_ALL)
                self.dbconn.logger.warn(Fore.GREEN+str(e)+Style.RESET_ALL)
        if track <= 0:
            print(Fore.RED+"Недопустимый путь"+Style.RESET_ALL)
        x =input(Fore.YELLOW+"Введите время прибытия или оставьте строку пустой для отмены"+Style.RESET_ALL)
        while not(self.time_validator(x)):
            x =input(Fore.YELLOW+"Введите время прибытия или оставьте строку пустой для отмены"+Style.RESET_ALL)
            if not x:
                return
        return [rid,sid,x,track]




    def show_route(self)->None:
        """
        отобразить полки
        """
        menu = Fore.YELLOW+""" Просмотр списка маршрутов
№\tМаршрут\tСтанция\tВремя\tпуть""" + Style.RESET_ALL
        print(Fore.YELLOW + menu + Style.RESET_ALL)
        lst = self.all()
        for i in lst:
            print(str(i[0]) + "\t" + str(i[1]) + "\t" + str(i[2]) + "\t" + str(i[3])+"\t" + str(i[4]))
        menu = Fore.YELLOW +"""Дальнейшие операции:
    """+Style.RESET_ALL +Fore.GREEN + str(0) + Style.RESET_ALL+"""  - возврат в главное меню;
    """+Fore.GREEN + str(3) + Style.RESET_ALL+"""  - добавление новой комнаты;
    """+Fore.GREEN + str(4) + Style.RESET_ALL+"""  - удаление комнаты;
    """+Fore.GREEN + str(5) + Style.RESET_ALL+"""  - просмотр стеллажей комнаты;
    """+Fore.GREEN + str(6) + Style.RESET_ALL+"""  - редактировать комнату
    """+Fore.GREEN + str(9) + Style.RESET_ALL+"""  - выход."""
        print(menu)
        return


    def add_route_attached_to_station(self)-> None:
        """
        обработчик создания полки
        """
        data = self.__call_creation_wizard()
        if type(data) == list:
            self.insert_one(data)
            print(Fore.GREEN + "маршрут создан"+ Style.RESET_ALL)

    def del_route_by_station(self,station_id:int):
        """
        удаление полки
        """
        lst = self.all_by_room_id(room_id)
        for i in lst:
            print(str(i[0]) + "\t" + str(i[1]) + "\t" + str(i[2]) + "\t" + str(i[3])+"\t" + str(i[4]))
            self.delete_shelf()
            self.all_by_room_id(station_id)





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

    def all_by_route_id(self, route_id:int):
        """
        Возвращает список полок по айди комнаты
        """
        if route_id not in self.create_list_of_routes():
            print(Fore.RED +"неверное значение, Выберите существующее" + Style.RESET_ALL)
        sql = "SELECT * FROM " + self.table_name()
        sql += " WHERE route_id = (%s)"
        cur = self.dbconn.conn.cursor()
        cur.execute(sql, (str(route_id),))
        return cur.fetchall()


    def edit_route(self):
        """
        редактор полок
        """
        inp = None
        col_2edit = None

        self.show_route()
        while not (inp in self.create_list_of_ids()):
            try:
                inp = int(input(Fore.YELLOW + "Выберите маршрут который хотите изменить для отмены введите 0: " + Style.RESET_ALL))
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




