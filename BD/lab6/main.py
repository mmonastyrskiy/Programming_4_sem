import sys
import colorama
sys.path.append('tables')
sys.path.append('lib')
from project_config import *
from dbconnection import *
from dbtable import DbTable
from room_table import RoomTable
from shelf_table import ShelfTable
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
        rt = RoomTable()
        st = ShelfTable()
        st.drop()
        rt.drop()
        rt.create()
        st.create()
        return

    def db_insert_somethings(self):
        """
        заполнение некими данными
        """
        rt = RoomTable()
        st = ShelfTable()
        rt.insert_one(['Room1',50,50,20,60,18,32])
        rt.insert_one(['Room2',500,500,40,100,22,32])
        rt.insert_one(['Room3',50,50,20,60,18,32])
        rt.insert_one(['Garage1',10000,10000,40,100,22,32])
        rt.insert_one(['Room4',50,50,20,60,18,32])

        st.insert_one([1,10,10,500,400,300,500,500])
        st.insert_one([1,50,50,500,400,400,600,600])
        st.insert_one([2,40,40,500,500,500,500,500])
        st.insert_one([3,40,40,500,500,500,500,500])
        st.insert_one([4,5,5,500,500,500,40,40])

    def db_drop(self):
        """
        drop структуры
        """
        rt = RoomTable()
        st = ShelfTable()
        st.drop()
        rt.drop()
        

    def show_main_menu(self):
        menu = Fore.YELLOW +"""Дальнейшие операции:
    """+Style.RESET_ALL +Fore.GREEN + str(1) + Style.RESET_ALL+"""  - взаимодействовать с комнатами
    """+Fore.GREEN + str(2) + Style.RESET_ALL+"""  - Очистка и создание таблиц
    """+Fore.GREEN + str(3) + Style.RESET_ALL+"""  - Взаимодействовать с полками
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
                RT = RoomTable()
                RT.delete_room()
                return "1"
            elif next_step == "7":
                print("Пока не реализовано!")
            elif next_step == '6':
                RT = RoomTable()
                RT.edit_room()
                next_step = "0"
            elif next_step == "3":
                RT = RoomTable()
                RT.add_rooms()
                next_step = "0"
            elif next_step == "5":
                ST = ShelfTable()
                RT = RoomTable()
                RT.show_rooms()
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
    """+Fore.GREEN + str(3) + Style.RESET_ALL+"""  - добавление новой полки к комнате;
    """+Fore.GREEN + str(4) + Style.RESET_ALL+"""  - удаление полки;
    """+Fore.GREEN + str(5) + Style.RESET_ALL+"""  - просмотр стеллажей комнаты;
    """+Fore.GREEN + str(6) + Style.RESET_ALL+"""  - редактирование полки
    """+Fore.GREEN + str(9) + Style.RESET_ALL + "  - выход."""

        print(menu)


        ST = ShelfTable()
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
            RT = RoomTable()
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
                RT = RoomTable()
                RT.show_rooms()
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
        DbTable.dbconn.test()

m = Main()
try:
    m.main_cycle()
except psycopg2.errors.UndefinedTable as UndefinedTable:
    print(Fore.RED +"Кажется заданная таблица не найдена, проверьте структуру базы данных или выполните действие 2 из главного меню, чтобы создать Таблицы\n" + Style.RESET_ALL
        , UndefinedTable)
except psycopg2.errors.CheckViolation:
    print(Fore.RED+"Нарушение ограничений целостности" + Style.RESET_ALL)
    m.main_cycle()
except Exception as e:
    print(e)
    try:
        connection.logger.warn(e)
    except Exception as e:
        print(Fore.RED+"лог файл недоступен"+Style.RESET_ALL)
    m.main_cycle()
