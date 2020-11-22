# Write your code here
from sqlalchemy import create_engine, Column, INTEGER, String, DATE
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime


DB_NAME = 'todo.db'
ENGINE_STR = 'sqlite:///{}?check_same_thread=False'

TODAY_TASK = '1'
ADD_TASK = '2'
EXIT = '0'

MENU_TEXT = """1) Today's tasks
2) Add task
0) Exit\n>"""


# define Table
engine = create_engine(ENGINE_STR.format(DB_NAME))
Base = declarative_base()


class Task(Base):
    __tablename__ = 'task'
    id = Column(INTEGER, primary_key=True)
    task = Column(String)
    deadline = Column(DATE, default=datetime.today())

    def __str__(self):
        return self.task


# create database
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)


def add_task():
    session = Session()
    task_detail = input("\nEnter task\n>")
    new_task = Task(task=task_detail)
    session.add(new_task)
    session.commit()
    print("The task has been added!\n")


def get_tasks():
    session = Session()
    tasks = session.query(Task).all()
    return tasks


def display_task(tasks_list):
    print("\nToday:")
    if tasks_list:
        txt = "{}. {}"
        for i, task in enumerate(tasks_list, start=1):
            print(txt.format(i, task))
        print()
    else:
        print("Nothing to do!\n")


def main():
    while True:
        choice = input(MENU_TEXT)
        if choice == TODAY_TASK:
            tasks = get_tasks()
            display_task(tasks)
        elif choice == ADD_TASK:
            add_task()
        elif choice == EXIT:
            break
        else:
            print("Invalid input.", end='\n\n')


if __name__ == '__main__':
    engine = ...
    main()
