# Write your code here
from datetime import timedelta, datetime
from base import Base, engine, Session
from models import Task


TODAY_TASK = '1'
WEEK_TASK = '2'
ALL_TASK = '3'
ADD_TASK = '4'
EXIT = '0'


MENU_TEXT = """1) Today's tasks
2) Week's tasks
3) All tasks
4) Add task
0) Exit\n>"""


def add_task(session):
    task_detail = input("\nEnter task\n>")
    deadline_str = input("Enter deadline\n>")
    deadline = datetime.strptime(deadline_str, "%Y-%m-%d")
    new_task = Task(task=task_detail, deadline=deadline)
    session.add(new_task)
    session.commit()
    print("The task has been added!\n")


def get_today_task(session):
    return get_tasks(session, TODAY_TASK)


def get_week_task(session):
    return get_tasks(session, WEEK_TASK)


def get_all_task(session):
    return get_tasks(session, ALL_TASK)


def get_tasks(session, period):
    if period == ALL_TASK:
        return session.query(Task).order_by(Task.deadline).all()
    elif period == WEEK_TASK:
        task_dict = {}
        today = datetime.today().date()
        for d in range(7):
            date = today + timedelta(days=d)
            task_dict[date] = session.query(Task).filter(Task.deadline == date).order_by(Task.deadline).all()
        return task_dict
    elif period == TODAY_TASK:
        today = datetime.today().date()
        return {today: session.query(Task).filter(Task.deadline == today).order_by(Task.deadline).all()}


def display_task(tasks):
    if isinstance(tasks, dict):
        if len(tasks) == 1:    # today task
            date, task_list = tasks.popitem()
            print("Today {}:".format(date.strftime("%d %b")))
            if not task_list:
                print("Nothing to do!\n")
            else:
                for i, task in enumerate(task_list, start=1):
                    print("{}. {}".format(i, task.task))
                print()
        else:  # week task
            for date, task_list in tasks.items():
                print("\n{}:".format(date.strftime("%A %d %b")))
                if not task_list:
                    print("Nothing to do!\n")
                else:
                    for i, task in enumerate(task_list, start=1):
                        print("{}. {}".format(i, task.task))
                    print()
    else:     # list of all tasks
        print("\nAll tasks:")
        if not tasks:
            print("Nothing to do!\n")
        else:
            for i, task in enumerate(tasks, start=1):
                print("{}. {}. {}".format(i, task.task, task.deadline.strftime("%d %b")))
            print()


def exit_program(session):
    session.commit()
    session.close()
    print("\nBye!")


def main():
    Base.metadata.create_all(engine)
    sess = Session()
    while True:
        choice = input(MENU_TEXT)
        if choice == TODAY_TASK:
            task_1day = get_today_task(sess)
            display_task(task_1day)
        elif choice == WEEK_TASK:
            task_of_week = get_week_task(sess)
            display_task(task_of_week)
        elif choice == ALL_TASK:
            tasks = get_all_task(sess)
            display_task(tasks)
        elif choice == ADD_TASK:
            add_task(sess)
        elif choice == EXIT:
            exit_program(sess)
            break
        else:
            print("Invalid input.", end='\n\n')


if __name__ == '__main__':
    main()
