import sys
import colorama
sys.path.append('tables')
sys.path.append('lib')
from project_config import *
from dbconnection import *
from dbtable import DbTable
from shedule_table import SheduleTable
from station_table import StationsTable
import psycopg2.errors
import colorama
from colorama import Fore, Back, Style

colorama.init()

class Main:

    config = ProjectConfig()
    connection = DbConnection(config)

    def __init__(self):
        DbTable.dbconn = self.connection
        return

    def db_init(self):
        """
        инициализация таблиц
        """
        rt = SheduleTable()
        st = StationsTable()
        st.drop()
        rt.drop()
        st.create()
        rt.create()
        return

    def db_insert_somethings(self):
        """
        заполнение некими данными
        """
        rt = SheduleTable()
        st = StationsTable()



        st.insert_one(['Бутово',1])
        st.insert_one(['Царицыно',2])
        st.insert_one(['Печатники',2])
        st.insert_one(['Новохохловская',3])
        st.insert_one(['Москва-товарная',3])
        st.insert_one(['Москва-Курская',3])
        st.insert_one(['Москва-Ярославская',3])
        st.insert_one(['Маленковская',3])
        st.insert_one(['Яуза',4])
        st.insert_one(['Ростокино',4])
        st.insert_one(['Мытищи',5])

        rt.insert_one([1,1,"12:00:00",2])
        rt.insert_one([1,3,'18:20:10',4])
        rt.insert_one([1,2,'22:15:30',3])
        rt.insert_one([2,4,'19:35:30',1])
        rt.insert_one([2,7,'05:00:00',2])

    def db_drop(self):
        """
        drop структуры
        """
        rt = SheduleTable()
        st = StationsTable()
        st.drop()
        rt.drop()
        

    def show_main_menu(self):
        menu = Fore.YELLOW +"""Дальнейшие операции:
    """+Style.RESET_ALL +Fore.GREEN + str(1) + Style.RESET_ALL+"""  - взаимодействовать с маршрутами
    """+Fore.GREEN + str(2) + Style.RESET_ALL+"""  - Очистка и создание таблиц
    """+Fore.GREEN + str(3) + Style.RESET_ALL+"""  - Взаимодействовать с станциями
    """+Fore.GREEN + str(9) + Style.RESET_ALL+"""  - выход."""
        print(menu)
        return

    def read_next_step(self):
        """
        отобразить приглашение ввода
        """
        return input(Fore.YELLOW +"=> " + Style.RESET_ALL).strip()

    def after_main_menu(self, next_step):
        """
        переход из главного меню
        """
        if next_step == "2":
            self.db_drop()
            self.db_init()
            self.db_insert_somethings()
            print(Fore.GREEN + "Таблицы созданы заново!"+ Style.RESET_ALL)
            return "0"
        elif next_step != "1" and next_step != "9" and next_step != "3":
            print(Fore.RED + "Выбрано неверное число! Повторите ввод!" + Style.RESET_ALL)

            return "0"
        else:
            return next_step
    def after_show_people(self, next_step):
        """
        меню комнат, обработка перехода
        """

        while True:
            if next_step == "4":
                RT = SheduleTable()
                RT.delete_station()
                return "1"
            elif next_step == "7":
                print("Пока не реализовано!")
            elif next_step == '6':
                RT = SheduleTable()
                RT.edit_route()
                next_step = "0"
            elif next_step == "3":
                RT = SheduleTable()
                RT.add_route_attached_to_station()
                next_step = "0"
            elif next_step == "5":
                ST = StationsTable()
                RT = SheduleTable()
                RT.show_route()
                rid = int(input(Fore.YELLOW +"выберите комнату для просмотра полок: " + Style.RESET_ALL))
                data = ST.all_by_room_id(rid)
                print(data)
                next_step = "0"
            elif next_step != "0" and next_step != "9" and next_step != "3":
                print(Fore.RED + "Выбрано неверное число! Повторите ввод!" + Style.RESET_ALL)
                return "1"
            else:
                return next_step
    def display_shelves_menu(self):
        """
         Меню полки + обработчик перехода
         """

        menu = Fore.YELLOW +"""Дальнейшие операции:
    """+Style.RESET_ALL +Fore.GREEN + str(0) + Style.RESET_ALL+"""  - возврта в главное меню
    """+Fore.GREEN + str(3) + Style.RESET_ALL+"""  - добавление новой станции к маршруту;
    """+Fore.GREEN + str(4) + Style.RESET_ALL+"""  - удаление станции;
    """+Fore.GREEN + str(5) + Style.RESET_ALL+"""  - просмотр станций комнаты;
    """+Fore.GREEN + str(6) + Style.RESET_ALL+"""  - редактирование полки
    """+Fore.GREEN + str(9) + Style.RESET_ALL + "  - выход."""

        print(menu)


        ST = StationsTable()
        user_chose = input(Fore.YELLOW +"выберите нужный пункт меню: " + Style.RESET_ALL)
        if user_chose == "0":
            return
        elif user_chose == "3":
            ST.add_shelf_attached_to_room()
            return
        elif user_chose == '4':
            ST.delete_shelf()
            ST.show_shelves()
            return
        elif user_chose == "5":
            RT = SheduleTable()
            RT.show_rooms()
            rid = int(input(Fore.YELLOW +"выберите комнату для просмотра полок: " + Style.RESET_ALL))
            data = ST.all_by_room_id(rid)
            print(data)
            return
        elif user_chose == "6":
            ST.edit_shelf()
            return
    def main_cycle(self):
        current_menu = "0"
        next_step = None
        while(current_menu != "9"):
            if current_menu == "0":
                self.show_main_menu()
                next_step = self.read_next_step()
                current_menu = self.after_main_menu(next_step)
            elif current_menu == "1":
                RT = SheduleTable()
                RT.show_route()
                next_step = self.read_next_step()
                current_menu = self.after_show_people(next_step)
            elif current_menu == "2":
                self.show_main_menu()
            elif current_menu == "3":
                self.display_shelves_menu()
                current_menu = "0"
        print(Fore.CYAN + "До свидания!"+Style.RESET_ALL)    
        return



    def test(self):
        DbTable.dbconn.teStationsTable()

m = Main()
m.main_cycle()
#try:
#    m.main_cycle()
#except psycopg2.errors.UndefinedTable as UndefinedTable:
#    print(Fore.RED +"Кажется заданная таблица не найдена, проверьте структуру базы данных или выполните действие 2 из главного меню, чтобы создать Таблицы\n" + Style.RESET_ALL
#        , UndefinedTable)
#except psycopg2.errors.CheckViolation:
#    print(Fore.RED+"Нарушение ограничений целостности" + Style.RESET_ALL)
#    m.main_cycle()
#except Exception as e:
#    print(Fore.RED+"Что-то пошло не так"+Style.RESET_ALL)
#    cur = m.connection.conn.cursor()
#    cur.execute("ROLLBACK TRANSACTION;")
#    try:
#        connection.logger.warn(e)
#    except Exception as e:
#        print(Fore.RED+"лог файл недоступен"+Style.RESET_ALL)
#    m.main_cycle()