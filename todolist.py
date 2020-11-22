# Write your code here
from datetime import timedelta, datetime
from base import Base, engine, Session
from item_menu import TodayTask, WeekTask, AllTask, MissedTask, AddTask, DeleteTask, ExitTask


class ToDoListApp:

    def __init__(self, menu_list):
        self.menu_map = {menu.task_number: menu for menu in menu_list}
        Base.metadata.create_all(engine)
        self.session = Session()

    def display_menu(self):
        for menu in self.menu_map.values():
            print("{}) {}".format(menu.task_number, menu))

    def run(self):
        stop = False
        while not stop:
            self.display_menu()
            choice = input('>')
            stop = self.menu_map[choice].execute(self.session)
        self.close()

    def close(self):
        self.session.commit()
        self.session.close()


def main():
    menu_list = [TodayTask(), WeekTask(), AllTask(), MissedTask(), AddTask(), DeleteTask(), ExitTask()]
    app = ToDoListApp(menu_list)
    app.run()


if __name__ == '__main__':
    main()
