from dbtable import *
import colorama
from colorama import Fore, Back, Style
import pglimits
colorama.init()
class StationsTable(DbTable):
    def table_name(self) -> str:
        """
    Возвращает строку схема + название таблицы
    """
        return self.dbconn.prefix + "stations"


    def columns(self)->dict:
        """
        Возвращает список полей + ограничения целостности на конкретные поля
        """
        return {"id": ["serial","PRIMARY KEY"],
    "name": ["character varying(100)", "NOT NULL"],
    "zone_id":["integer", "NOT NULL"]
    }


    def table_constraints (self)->list:
        """
        Возвращает список общих ограничений целостности
        """
        return []



    def delete_station(self)->None:
        id_ = None
        """
        Отрабатывает удаление комнаты
        """
        while not ((type(id_) == int) and (id_ in self.create_list_of_ids())):
            try:
                id_ = int(input(Fore.YELLOW +"Введите номер станции, которую хотите удалить (введите -1 для отмены): " + Style.RESET_ALL).strip())
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


    def show_station(self)->None:
        """
        отобразить список комнат в терминал
        """
        menu = """Просмотр списка комнат!
№\tИмя\tЗона\t"""
        print(Fore.YELLOW + menu + Style.RESET_ALL)
        lst = self.all()
        for i in lst:
            print(Fore.GREEN+str(i[0])+Style.RESET_ALL + "\t" + str(i[1]) + "\t" + str(i[2]))
        menu = Fore.YELLOW +"""Дальнейшие операции:
    """+Style.RESET_ALL +Fore.GREEN + str(0) + Style.RESET_ALL+"""  - возврат в главное меню;
    """+Fore.GREEN + str(3) + Style.RESET_ALL+"""  - добавление новой станции;
    """+Fore.GREEN + str(4) + Style.RESET_ALL+"""  - удаление станции;
    """+Fore.GREEN + str(5) + Style.RESET_ALL+"""  - просмотр поездов, которые останавливаются на станции;
    """+Fore.GREEN + str(6) + Style.RESET_ALL+"""  - редактировать станцию
    """+Fore.GREEN + str(9) + Style.RESET_ALL+"""  - выход."""
        print(menu)
        return


    def __call_creation_wizard(self)->list:
        name = ""
        zone_id = None
        """
        Запуск мастера создания комнаты
        """
        while not (0< len(name) <= pglimits.VARCHAR_MAX):
            try:
                name = input(Fore.YELLOW+ "Введите название станции или пустую строку для отмены: " + Style.RESET_ALL)
                if not(len(name)):
                    return
                if (len(name) > pglimits.VARCHAR_MAX):
                    raise ValueError
            except ValueError:
                print(Fore.RED + "Строка слишком большая" + Style.RESET_ALL)

        while not ((type(zone_id) == int) and (pglimits.NUMERIC7_2_MIN <= zone_id <= pglimits.PG_INT_MAX)):
            try:
                zone_id = int(input(Fore.YELLOW+ "Введите зону станции для отмены введите 0: " + Style.RESET_ALL))
                if not zone_id:
                    return
                if not (0 < zone_id <= pglimits.PG_INT_MAX):
                    raise ValueError
            except ValueError as e:
                print(Fore.RED+"Введено неверное число" + Style.RESET_ALL)
                self.dbconn.logger.warn(Fore.GREEN+str(e)+Style.RESET_ALL)


        return [name,zone_id]
        




    def add_station(self)-> None:
        """
        обработчик создания комнаты
        """
        data = self.__call_creation_wizard()
        if type(data) == list:
            self.insert_one(data)
            print(Fore.GREEN + "станция создана"+ Style.RESET_ALL)


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
            try:
                sql = "UPDATE " + self.table_name() + " SET " +self.column_names_without_id()[col_2edit]
                sql += " = (%s) WHERE " + self.primary_key()[0] + " = (%s)"
                cur = self.dbconn.conn.cursor()
                if not(0<int(new_data)<=pglimits.PG_INT_MAX):
                    raise ValueError
            except ValueError as e:
                print(Fore.RED +"Введено неверное значение" + Style.RESET_ALL)
                new_data = input(Fore.YELLOW + "Введите заново: "+ Style.RESET_ALL)
                self.dbconn.logger.warn(Fore.GREEN+str(e)+Style.RESET_ALL)
                self.edit_check(id_,col_2edit,new_data)

            cur.execute(sql, [new_data, str(id_)])
            self.dbconn.conn.commit()
            return True


    def edit_station(self):
        inp = None
        col_2edit = None
        """
        Изменение параметров существующей сущности комнаты
        """
        self.show_rooms()
        while not (inp in self.create_list_of_ids()):
            try:
                inp = int(input(Fore.YELLOW+"Выберите станцию которую хотите изменить: "+Style.RESET_ALL))
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


