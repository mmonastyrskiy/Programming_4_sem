import sys
sys.path.append('tables')

from project_config import *
from dbconnection import *
from dbtable import DbTable
from room_table import RoomTable
from shelf_table import ShelfTable

class Main:

    config = ProjectConfig()
    connection = DbConnection(config)

    def __init__(self):
        DbTable.dbconn = self.connection
        return

    def db_init(self):
        rt = RoomTable()
        st = ShelfTable()
        st.drop()
        rt.drop()
        rt.create()
        st.create()
        return

    def db_insert_somethings(self):
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
        rt = RoomTable()
        st = ShelfTable()
        st.drop()
        rt.drop()
        

    def show_main_menu(self):
        menu = """Добро пожаловать! 
Основное меню (выберите цифру в соответствии с необходимым действием): 
    1 - взаимодействовать с комнатами;
    2 - сброс и инициализация таблиц;
    3 - взаимодействовать с полками
    9 - выход."""
        print(menu)
        return

    def read_next_step(self):
        return input("=> ").strip()

    def after_main_menu(self, next_step):
        if next_step == "2":
            self.db_drop()
            self.db_init()
            self.db_insert_somethings()
            print("Таблицы созданы заново!")
            return "0"
        elif next_step != "1" and next_step != "9" and next_step != "3":
            print("Выбрано неверное число! Повторите ввод!")

            return "0"
        else:
            return next_step
    def after_show_people(self, next_step):

        while True:
            if next_step == "4":
                RT = RoomTable()
                RT.delete_room()
                return "1"
            elif next_step == "6" or next_step == "7":
                print("Пока не реализовано!")
                next_step = "5"
            elif next_step == "5":
                next_step = self.show_phones_by_people()
            elif next_step != "0" and next_step != "9" and next_step != "3":
                print("Выбрано неверное число! Повторите ввод!")
                return "1"
            else:
                return next_step
    def display_shelves_menu(self):
        menu = """Дальнейшие операции:
        0 - возврат в главное меню;
        3 - добавление новой полки к комнате;
        4 - удаление полки;
        5 - просмотр стеллажей комнаты;
        9 - выход."""
        print(menu)
        ST = ShelfTable()
        user_chose = input("выберите нужный пункт меню: ")
        if user_chose == "0":
            return
        elif user_chose == "3":
            ST.add_shelf_attached_to_room()
            return
        elif user_chose == '4':
            ST.delete_shelf()
            return
        elif user_chose == "5":
            RT = RoomTable()
            RT.show_rooms()
            rid = int(input("выберите комнату для просмотра полок: "))
            ST.all_by_room_id(rid)
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
        print("До свидания!")    
        return

    def test(self):
        DbTable.dbconn.test()

m = Main()
m.main_cycle()
