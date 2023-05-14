from dbtable import *
import colorama
from colorama import Fore, Back, Style
import pglimits
colorama.init()
class RoomTable(DbTable):
    def table_name(self) -> str:
        """
    Возвращает строку схема + название таблицы
    """
        return self.dbconn.prefix + "Room"


    def columns(self)->dict:
        """
        Возвращает список полей + ограничения целостности на конкретные поля
        """
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
        """
        Возвращает список общих ограничений целостности
        """
        return ([
        "CONSTRAINT uni_room_name UNIQUE (name)",
	   "CONSTRAINT positive_volume_left_room CHECK(space_left >0)",
	   "CONSTRAINT positive_volume_room CHECK(space >0)",
	   "CONSTRAINT volume_left_le_volume CHECK(space_left <= space)",
	   "CONSTRAINT hu_max_in_interval CHECK (max_humidity <= 100 and max_humidity >= 0)",
	   "CONSTRAINT hu_min_in_interval CHECK (min_humidity <= 100 and min_humidity >= 0)",
       "CONSTRAINT temp_check CHECK (min_temp <= max_temp)",
       "CONSTRAINT hu_check CHECK (min_humidity <= max_humidity)"

       ])



    def delete_room(self)->None:
        id_ = None
        """
        Отрабатывает удаление комнаты
        """
        while not ((type(id_) == int) and (id_ in self.create_list_of_ids())):
            try:
                id_ = int(input(Fore.YELLOW +"Введите номер комнаты, которую хотите удалить (введите -1 для отмены): " + Style.RESET_ALL).strip())
                if id_ == -1:
                    return
                if id_ not in self.create_list_of_ids():
                    raise ValueError
            except ValueError as e:
                print(Fore.RED +"Введите номер по списку, введеное значение - не число" + Style.RESET_ALL)
                self.dbconn.logger.warn(Fore.GREEN+str(e)+Style.RESET_ALL)
        sql = "DELETE FROM " + self.table_name()
        sql += f" WHERE id = (%s)"
        cur = self.dbconn.conn.cursor()
        id_ = str(id_)
        cur.execute(sql, (id_,))
        self.dbconn.conn.commit()
        self.show_rooms()


    def show_rooms(self)->None:
        """
        отобразить список комнат в терминал
        """
        menu = """Просмотр списка комнат!
№\tИмя\tОбъем\t"""
        print(Fore.YELLOW + menu + Style.RESET_ALL)
        lst = self.all()
        for i in lst:
            print(Fore.GREEN+str(i[0])+Style.RESET_ALL + "\t" + str(i[1]) + "\t" + str(i[2]))
        menu = Fore.YELLOW +"""Дальнейшие операции:
    """+Style.RESET_ALL +Fore.GREEN + str(0) + Style.RESET_ALL+"""  - возврат в главное меню;
    """+Fore.GREEN + str(3) + Style.RESET_ALL+"""  - добавление новой комнаты;
    """+Fore.GREEN + str(4) + Style.RESET_ALL+"""  - удаление комнаты;
    """+Fore.GREEN + str(5) + Style.RESET_ALL+"""  - просмотр стеллажей комнаты;
    """+Fore.GREEN + str(6) + Style.RESET_ALL+"""  - редактировать комнату
    """+Fore.GREEN + str(9) + Style.RESET_ALL+"""  - выход."""
        print(menu)
        return


    def __call_creation_wizard(self)->list:
        name = ""
        space = None
        minh=maxh = None
        mint=maxt = None
        """
        Запуск мастера создания комнаты
        """
        while not (0< len(name) <= pglimits.VARCHAR_MAX):
            try:
                name = input(Fore.YELLOW+ "Введите название комнаты или пустую строку для отмены: " + Style.RESET_ALL)
                if not(len(name)):
                    return
                if (len(name) > pglimits.VARCHAR_MAX):
                    raise ValueError
            except ValueError:
                print(Fore.RED + "Строка слишком большая" + Style.RESET_ALL)

        while not ((type(space) == float) and (pglimits.NUMERIC7_2_MIN <= space <= pglimits.NUMERIC7_2_MAX)):
            try:
                space = float(input(Fore.YELLOW+ "Введите объем комнаты для отмены введите 0: " + Style.RESET_ALL))
                if not space:
                    return
                if (space < 0) or not (pglimits.NUMERIC7_2_MIN <= space <= pglimits.NUMERIC7_2_MAX):
                    raise ValueError
            except ValueError as e:
                print(Fore.RED+"Введено неверное число" + Style.RESET_ALL)
                self.dbconn.logger.warn(Fore.GREEN+str(e)+Style.RESET_ALL)

        
        while not ((type(minh)==float) and (type(maxh)==float) and (0< minh <= 100) and (0 < maxh <= 100) and minh <= maxh):
            try:
                minh = float(input(Fore.YELLOW+ "Введите минимальную влажность для отмены введите 0: " + Style.RESET_ALL))
                if not(minh):
                    return
                maxh = float(input(Fore.YELLOW+ "Введите максимальную влажность для отмены введите 0: " + Style.RESET_ALL))
                if not (maxh):
                    return
                if not((0< minh <= 100) and (0 < maxh <= 100) and minh <= maxh):
                    raise ValueError
            except ValueError as e:
                print(Fore.RED+ "Одна или обе из влажностей введена(ы) неверно"+Style.RESET_ALL)
                self.dbconn.logger.warn(Fore.GREEN+str(e)+Style.RESET_ALL)

        while not ((type(mint)==float) and (type(maxt)==float) and (0< mint <= 100) and (0 < maxt <= 100) and mint <= maxt):
            try:
                mint = float(input(Fore.YELLOW+ "Введите минимальную температуру для отмены введите 0: " + Style.RESET_ALL))
                if not mint:
                    return
                maxt = float(input(Fore.YELLOW+ "Введите максимальную температуру для отмены введите 0: " + Style.RESET_ALL))
                if not maxt:
                    return
                if not((0< mint <= 100) and (0 < maxt <= 100) and mint <= maxt):
                    raise ValueError
            except ValueError as e:
                print(Fore.RED + "Одна или обе из температур введена(ы) неверно"+Style.RESET_ALL)
                self.dbconn.logger.warn(Fore.GREEN+str(e)+Style.RESET_ALL)
        return [name,space,space,minh,maxh,mint,maxt]
        




    def add_rooms(self)-> None:
        """
        обработчик создания комнаты
        """
        data = self.__call_creation_wizard()
        if type(data) == list:
            self.insert_one(data)
            print(Fore.GREEN + "Комната создана"+ Style.RESET_ALL)


    def edit_check(self,id_:int, col_2edit: int, new_data:str)-> bool:
        """
        Контроль за соблюдением ограничений целостности при изменении полей в методе edit_room
        """
        if(col_2edit == 0):
            try:
                if len(new_data) > pglimits.VARCHAR_MAX:
                    raise ValueError
            except ValueError:
                    print(Fore.RED + "Строка слишком большая" + Style.RESET_ALL)
                    new_data = input(Fore.YELLOW + "Введите заново: "+ Style.RESET_ALL)
                    return self.edit_check(id_,col_2edit,new_data)
            sql = "UPDATE " + self.table_name() + " SET " +self.column_names_without_id()[col_2edit]
            sql += " = (%s) WHERE " + self.primary_key()[0] + " = (%s)"
            cur = self.dbconn.conn.cursor()
            cur.execute(sql, [new_data, str(id_,)])
            self.dbconn.conn.commit()
            return True
        elif (col_2edit == 1):
            sql = "UPDATE " + self.table_name() + " SET " +self.column_names_without_id()[col_2edit]
            sql += " = (%s) WHERE " + self.primary_key()[0] + " = (%s)"
            cur = self.dbconn.conn.cursor()
            try:
                sql = f"SELECT {self.column_names_without_id()[col_2edit+1]} FROM {self.table_name()} WHERE {self.primary_key()[0]} = (%s)"
                cur = self.dbconn.conn.cursor()
                cur.execute(sql, (str(id_),))
                recived = list(cur.fetchone())[0]

                if (not(float(new_data) >= recived) or (float(new_data) <= 0) or 
                    not(pglimits.NUMERIC7_2_MIN<= float(new_data) <= pglimits.NUMERIC7_2_MAX)):
                    raise ValueError
            except ValueError as e:
                print(Fore.RED +"Введено неверное значение" + Style.RESET_ALL)
                new_data = input(Fore.YELLOW + "Введите заново: "+ Style.RESET_ALL)
                return self.edit_check(id_,col_2edit,new_data)

                self.dbconn.logger.warn(Fore.GREEN+str(e)+Style.RESET_ALL)

            cur.execute(sql, [new_data, str(id_)])
            self.dbconn.conn.commit()
            return True
        elif (col_2edit == 3):
            sql = "UPDATE " + self.table_name() + " SET " +self.column_names_without_id()[col_2edit]
            sql += " = (%s) WHERE " + self.primary_key()[0] + " = (%s)"
            cur = self.dbconn.conn.cursor()
            try:
                d = float(new_data)
                min_ = f"SELECT {self.column_names_without_id()[-3]} FROM " + self.table_name() + f" WHERE {self.primary_key()[0]} = {str(id_)}"
                cur.execute(min_)
                r = float(cur.fetchone()[0])

                if not ((0 <= d <= 100)) or (d > r):
                    raise ValueError
            except ValueError as e:
                self.dbconn.logger.warn(Fore.GREEN+str(e)+Style.RESET_ALL)
                print(Fore.RED +"Введено неверное значение" + Style.RESET_ALL)
                new_data = input(Fore.YELLOW + "Введите заново: "+ Style.RESET_ALL)
                return self.edit_check(id_,col_2edit,new_data)
            cur.execute(sql, [new_data, str(id_)])
            self.dbconn.conn.commit()
            return True
        elif (col_2edit == 4):
            sql = "UPDATE " + self.table_name() + " SET " +self.column_names_without_id()[col_2edit]
            sql += " = (%s) WHERE " + self.primary_key()[0] + " = (%s)"
            cur = self.dbconn.conn.cursor()
            try:
                d = float(new_data)
                min_ = f"SELECT {self.column_names_without_id()[-4]} FROM " + self.table_name() + f" WHERE {self.primary_key()[0]} = {str(id_)}"
                cur.execute(min_)
                r = float(cur.fetchone()[0])

                if not ((0 <= d <= 100)) or (d < r):
                    raise ValueError
            except ValueError as e:
                self.dbconn.logger.warn(Fore.GREEN+str(e)+Style.RESET_ALL)
                print(Fore.RED +"Введено неверное значение" + Style.RESET_ALL)
                new_data = input(Fore.YELLOW + "Введите заново: "+ Style.RESET_ALL)
                return self.edit_check(id_,col_2edit,new_data)
            cur.execute(sql, [new_data, str(id_)])
            self.dbconn.conn.commit()
            return True
        elif (col_2edit == 5):
            sql = "UPDATE " + self.table_name() + " SET " +self.column_names_without_id()[col_2edit]
            sql += " = (%s) WHERE " + self.primary_key()[0] + " = (%s)"
            cur = self.dbconn.conn.cursor()
            try:
                d = float(new_data)
                min_ = f"SELECT {self.column_names_without_id()[-1]} FROM " + self.table_name() + f" WHERE {self.primary_key()[0]} = {str(id_)}"
                cur.execute(min_)
                r = float(cur.fetchone()[0])
                if not ((0 <= d <= 100)) or (d > r):
                    raise ValueError
            except ValueError as e:
                self.dbconn.logger.warn(Fore.GREEN+str(e)+Style.RESET_ALL)
                print(Fore.RED +"Введено неверное значение" + Style.RESET_ALL)
                new_data = input(Fore.YELLOW + "Введите заново: "+ Style.RESET_ALL)
                return self.edit_check(id_,col_2edit,new_data)
            cur.execute(sql, [new_data, str(id_)])
            self.dbconn.conn.commit()
            return True
        elif (col_2edit == 6):
            sql = "UPDATE " + self.table_name() + " SET " +self.column_names_without_id()[col_2edit]
            sql += " = (%s) WHERE " + self.primary_key()[0] + " = (%s)"
            cur = self.dbconn.conn.cursor()
            try:
                d = float(new_data)
                min_ = f"SELECT {self.column_names_without_id()[-2]} FROM " + self.table_name() + f" WHERE {self.primary_key()[0]} = {str(id_)}"
                cur.execute(min_)
                r = float(cur.fetchone()[0])
                if not ((0 <= d <= 100)) or (d < r):
                    raise ValueError
            except ValueError as e:
                self.dbconn.logger.warn(Fore.GREEN+str(e)+Style.RESET_ALL)
                print(Fore.RED +"Введено неверное значение" + Style.RESET_ALL)
                new_data = input(Fore.YELLOW + "Введите заново: "+ Style.RESET_ALL)
                return self.edit_check(id_,col_2edit,new_data)
            cur.execute(sql, [new_data, str(id_)])
            self.dbconn.conn.commit()
            return True
        else:
            print(Fore.RED+"Ошибка, затронут неверный столбец, возможно неизменяемый"+Style.RESET_ALL)
            return False



    def edit_room(self):
        inp = None
        col_2edit = None
        """
        Изменение параметров существующей сущности комнаты
        """
        self.show_rooms()
        while not (inp in self.create_list_of_ids()):
            try:
                inp = int(input(Fore.YELLOW+"Выберите комнату которую хотите изменить: "+Style.RESET_ALL))
                if inp not in self.create_list_of_ids():
                    raise ValueError
            except ValueError as e:
                print(Fore.RED+"Введите правильное число"+Style.RESET_ALL)
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
                col_2edit = int(input(Fore.YELLOW+"Введите номер поля, который хотите изменить: " + Style.RESET_ALL))
                if not(0 <= col_2edit < len(data)):
                    raise ValueError
            except ValueError as e:
                print(Fore.RED+"Введено неверное число"+Style.RESET_ALL)
                self.dbconn.logger.warn(Fore.GREEN+str(e)+Style.RESET_ALL)
        new_data = input(Fore.YELLOW+"Введите новое значение поля: "+Style.RESET_ALL)
        if self.edit_check(inp,col_2edit,new_data):
            print(Fore.GREEN+"Изменения применены"+Style.RESET_ALL)
            return
        print(Fore.RED+"Во внесении изменений отказно, неверное новое значение"+Style.RESET_ALL)
        return

