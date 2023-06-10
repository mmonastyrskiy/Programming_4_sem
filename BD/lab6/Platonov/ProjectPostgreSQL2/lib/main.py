import sys

sys.path.append('tables')

from lib.project_config import *
from lib.dbconnection import *
from tables.car_table import *
from tables.driver_table import *


class Main:
    config = ProjectConfig()
    connection = DbConnection(config)

    def __init__(self):
        DbTable.dbconn = self.connection
        self.driver_list = []
        return

    def db_init(self):
        pt = DriveTable()
        pht = CarTable()
        pt.create()
        pht.create()
        return

    def db_insert_somethings(self):
        pt = DriveTable()
        pht = CarTable()
        pt.insert_one([1, "Муравенко", "Павел", "Петрович", '27.11.2003', 121232, "MM", 111])
        pt.insert_one([2, "Муравенко2", "Павел2", "Петрович2", '28.11.2003', 11232, "MM", 222])
        pt.insert_one([3, "Муравенко", "Павел", "Петрович", '27.11.2003', 121232, "MM", 333])

        pht.insert_one([1, "polo", "эконом", "1111", "1978", 1])
        pht.insert_one([2, "porche", "бизнес", "2222", "1976", 2])
        pht.insert_one([3, "golf", "комфорт", "3333", "2004", 3])

    def db_drop(self):
        pht = CarTable()
        pt = DriveTable()
        pht.drop()
        pt.drop()
        return

    def show_main_menu(self):
        menu = """Добро пожаловать! 
Основное меню (выберите цифру в соответствии с необходимым действием): 
    1 - просмотр водителей;
    2 - сброс и инициализация таблиц;
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
        elif next_step != "1" and next_step != "9":
            print("Выбрано неверное число! Повторите ввод!")
            return "0"
        else:
            return next_step

    def show_drivers(self):
        self.id_driver = -1
        menu = """Просмотр списка водителей!
№\tФамилия\tИмя\tОтчество\tДень Рождения\tИНН\tСерия Паспорта\tНомер Паспорта"""
        print(menu)
        lst = DriveTable().all()
        for i in lst:
            print(str(i[0]) + "\t" + str(i[1]) + "\t" + str(i[2]) + "\t" + str(i[3]) + "\t" + str(i[4]) + "\t" + str(
                i[5]) + "\t" + str(
                i[6]) + "\t" + str(i[7]))
        menu = """Дальнейшие операции: 
    0 - возврат в главное меню;
    3 - добавление нового водителя;
    4 - удаление водителя;
    5 - просмотр машины водителя ;
    9 - выход."""
        print(menu)
        return

    def after_show_drivers(self, next_step):
        while True:
            if next_step == "4":
                pt = DriveTable()
                inp = input('Введите id водителя которую хотите удалить: ').strip()
                pt.delete_by_id_drivers(inp)
                return "1"
            elif next_step == "6":  ##удаление и добавление стеллажей
                next_step = self.show_add_car()
            elif next_step == "7":
                l = CarTable()
                inp = int(input('Введите id машины который хотите удалить: ').strip())
                l.delete_car(inp)
                return "1"
            elif next_step == "5":
                next_step = self.show_cars_by_drivers()
            elif next_step != "0" and next_step != "9" and next_step != "3":
                print("Выбрано неверное число! Повторите ввод!")
                return "1"
            else:
                return next_step

    def show_add_car(self):
        data = ["0"] * 6
        data[0] = (input("Введите Марку (1 - отмена): ").strip())
        if data[0] == "1":
            return
        while len(data[0].strip()) == 0:
            data[0] = input(
                "Поле Марка не может быть пустым! Введите Марку заново (1 - отмена):").strip()
            if data[0] == "1":
                return

        data[1] = (input("Введите Класс (1 - отмена): ").strip())
        if data[1] == "1":
            return "1"
        while len(data[1].strip()) == 0:
            data[1] = input("Поле Класс не может быть пустым! Введите Класс заново (1 - отмена):").strip()
            if data[1] == "1":
                return "1"

        data[2] = (input("Введите Цвет (1 - отмена): ").strip())
        if data[2] == "1":
            return "1"
        while len(data[2].strip()) == 0:
            data[2] = input("Поле Цвет не может быть пустым! Введите Цвет заново (1 - отмена):").strip()
            if data[2] == "1":
                return "1"

        data[3] = (input("Введите Гос.номер (1 - отмена): ").strip())
        if data[3] == "1":
            return "1"
        while len(data[3].strip()) == 0:
            data[3] = input("Поле Гос.номер не может быть пустым! Введите Гос.номер заново (1 - отмена):").strip()
            if data[3] == "1":
                return "1"

        data[4] = (input("Введите Год выпуска (1 - отмена): ").strip())
        if data[4] == "1":
            return "1"
        while len(data[4].strip()) == 0:
            data[4] = input(
                "Поле Год выпуска не может быть пустым! Введите Год выпуска заново (1 - отмена):").strip()
            if data[4] == "1":
                return "1"

        data[5] = (input("Введите id водителя, который поедет на этой машине (1 - отмена): ").strip())
        if data[5] == "1":
            return "1"
        while len(data[5].strip()) == 0:
            data[5] = input(
                "Поле id водителя, который поедет на этой машине не может быть пустым! Введите id водителя, который поедет на этой машине заново (1 - отмена):").strip()
            if data[5] == "1":
                return "1"

        # RackTable().insert_one(data)
        print(data)
        CarTable().add_car(data[0], data[1], data[2], data[3], data[4], data[5])
        return "0"

    def show_add_driver(self):
        data = ["0"] * 7
        data[0] = (input("Введите Фамилию (1 - отмена): ").strip())
        if data[0] == "1":
            return
        while len(data[0].strip()) == 0:
            data[0] = input(
                "Поле Фамилия не может быть пустым! Введите Фамилию заново (1 - отмена):").strip()
            if data[0] == "1":
                return

        data[1] = (input("Введите Имя (1 - отмена): ").strip())
        if data[1] == "1":
            return "1"
        while len(data[1].strip()) == 0:
            data[1] = input("Поле Имя не может быть пустым! Введите Имя заново (1 - отмена):").strip()
            if data[1] == "1":
                return "1"

        data[2] = (input("Введите Отчество (1 - отмена): ").strip())
        if data[2] == "1":
            return "1"
        while len(data[2].strip()) == 0:
            data[2] = input("Поле Отчество не может быть пустым! Введите Отчество заново (1 - отмена):").strip()
            if data[2] == "1":
                return "1"

        data[3] = (input("Введите День рождения (1 - отмена): ").strip())
        if data[3] == "1":
            return "1"
        while len(data[3].strip()) == 0:
            data[3] = input(
                "Поле День рождения не может быть пустым! Введите День рождения заново (1 - отмена):").strip()
            if data[3] == "1":
                return "1"

        data[4] = (input("Введите ИНН (1 - отмена): ").strip())
        if data[4] == "1":
            return "1"
        while len(data[4].strip()) == 0:
            data[4] = input(
                "Поле ИНН выпуска не может быть пустым! Введите ИНН заново (1 - отмена):").strip()
            if data[4] == "1":
                return "1"

        data[5] = (input("Введите Серию паспорта (1 - отмена): ").strip())
        if data[5] == "1":
            return "1"
        while len(data[5].strip()) == 0:
            data[5] = input(
                "Поле Серия паспорта не может быть пустым! Введите Серию паспорта заново (1 - отмена):").strip()
            if data[5] == "1":
                return "1"

        data[6] = (input("Введите Номер паспорта (1 - отмена): ").strip())
        if data[6] == "1":
            return "1"
        while len(data[6].strip()) == 0:
            data[6] = input(
                "Поле Номер паспорта не может быть пустым! Введите Номер паспорта заново (1 - отмена):").strip()
            if data[6] == "1":
                return "1"

        # RackTable().insert_one(data)
        print(data)
        DriveTable().add_driver(data[0], data[1], data[2], data[3], data[4], data[5], data[6])
        return "0"

    #
    def show_cars_by_drivers(self):
        if not self.driver_list:  # Если список водителей пуст, запрашиваем данные у пользователя
            while True:
                num = input("Укажите номер строки, в которой записан интересующий Вас водитель (0 - отмена):")
                while len(num.strip()) == 0:
                    num = input(
                        "Пустая строка. Повторите ввод! Укажите номер строки, в которой записан интересующий Вас водитель (0 - отмена):")
                if num == "0":
                    return "1"
                driver = DriveTable().find_by_position(int(num))
                print(driver)
                if not driver:
                    print("Введено число, неудовлетворяющее количеству водителей!")
                else:
                    self.driver_list.append(driver)  # Добавляем выбранного водителя в список
                    break

        print("Выбран водитель:")
        for driver in self.driver_list:
            print(str(driver[0]) + " " + str(driver[1]) + " " + str(driver[2]) + " " + str(driver[3]) + " " + driver[
                4] + " " + driver[5] + " " + driver[6] + " " + driver[7])
        menu = """Дальнейшие операции:
    0 - возврат в главное меню;
    1 - возврат в просмотр людей;
    6 - добавление нового телефона;
    7 - удаление телефона;
    9 - выход."""
        print(menu)
        return self.read_next_step()

        return self.read_next_step()

    def main_cycle(self):
        current_menu = "0"
        next_step = None
        while (current_menu != "9"):
            if current_menu == "0":
                self.show_main_menu()
                next_step = self.read_next_step()
                current_menu = self.after_main_menu(next_step)
            elif current_menu == "1":
                self.show_drivers()
                next_step = self.read_next_step()
                current_menu = self.after_show_drivers(next_step)
            elif current_menu == "2":
                self.show_main_menu()
            elif current_menu == "3":
                self.show_add_driver()
                current_menu = "1"
        print("До свидания!")
        return

    def test(self):
        DbTable.dbconn.test()


m = Main()
# m.db_init()
# Откоментируйте эту строку и закоментируйте следующую для теста
# соединения с БД
m.test()
m.main_cycle()
