from datetime import datetime, timedelta
from models import Task


TODAY_TASK = '1'
WEEK_TASK = '2'
ALL_TASK = '3'
MISS_TASK = '4'
ADD_TASK = '5'
DELETE_TASK = '6'
EXIT = '0'


class MenuItem:

    name = 'MenuItem'
    task_number = None
    stop = False

    @staticmethod
    def get_data(session=None):
        pass

    def display(self, tasks=None):
        pass

    def execute(self, session):
        pass

    def __str__(self):
        return self.name


class AllTask(MenuItem):

    name = "All tasks"
    header = "All tasks"
    no_task = "Nothing to do!"
    task_number = ALL_TASK

    @staticmethod
    def get_data(session=None):
        return session.query(Task).order_by(Task.deadline).all()

    def display(self, tasks=None):
        msg = "\n{}:".format(self.header)
        if not tasks:
            print(msg + "\n{}\n".format(self.no_task))
        else:
            print(msg + "\n" + "\n".join("{}. {}. {}".format(i, task.task, task.deadline.strftime("%d %b")) for i, task in enumerate(tasks, start=1)), end='\n\n')

    def execute(self, session):
        tasks = self.get_data(session)
        self.display(tasks)
        return self.stop


class MissedTask(AllTask):

    name = "Missed tasks"
    header = "Missed tasks:"
    no_task = "Nothing is missed!"
    task_number = MISS_TASK

    @staticmethod
    def get_data(session=None):
        today = datetime.today().date()
        return session.query(Task).filter(Task.deadline < today).order_by(Task.deadline).all()


class DeleteTask(AllTask):
    name = "Delete task"
    header = "Choose the number of the task you want to delete:"
    no_task = "Nothing to delete"
    success = "The task has been deleted!"
    task_number = DELETE_TASK

    def execute(self, session):
        tasks = self.get_data(session)
        if tasks:
            self.display(tasks)
            choice = int(input(">"))
            assert choice <= len(tasks)
            task_to_delete = tasks[choice - 1]
            session.delete(task_to_delete)
            session.commit()
            print(self.success, end='\n\n')
        else:
            print(self.no_task)
        return self.stop


class TodayTask(MenuItem):

    name = "Today's tasks"
    header = "Today {}:"
    no_task = "Nothing to do!"
    task_number = TODAY_TASK

    @staticmethod
    def get_data(session=None):
        today = datetime.today().date()
        return session.query(Task).filter(Task.deadline == today).order_by(Task.deadline).all()

    def display(self, tasks=None):
        date = datetime.today()
        msg = self.header.format(date.strftime("%d %b"))
        if not tasks:
            msg += "\n{}\n".format(self.no_task)
            print(msg)
        else:
            msg = msg + '\n' + "\n".join("{}. {}".format(i, task.task) for i, task in enumerate(tasks, start=1)) + "\n"
            print(msg)

    def execute(self, session):
        tasks = self.get_data(session)
        self.display(tasks)
        return self.stop


class WeekTask(MenuItem):
    name = "Week's tasks"
    header = ""
    no_task = "Nothing to do!"
    task_number = WEEK_TASK

    @staticmethod
    def get_data(session=None):
        task_dict = {}
        today = datetime.today().date()
        for d in range(7):
            date = today + timedelta(days=d)
            task_dict[date] = session.query(Task).filter(Task.deadline == date).order_by(Task.deadline).all()
        return task_dict

    def display(self, tasks=None):
        for date, task_list in tasks.items():
            print("\n{}:".format(date.strftime("%A %d %b")))
            if not task_list:
                print(self.no_task)
            else:
                for i, task in enumerate(task_list, start=1):
                    print("{}. {}".format(i, task.task))
                print()

    def execute(self, session):
        tasks = self.get_data(session)
        self.display(tasks)
        return self.stop


class AddTask(MenuItem):
    name = 'Add task'
    success = "The task has been added!"
    task_number = ADD_TASK

    @staticmethod
    def get_data(session=None):
        task_detail = input("\nEnter task\n>")
        deadline_str = input("Enter deadline\n>")
        deadline = datetime.strptime(deadline_str, "%Y-%m-%d")
        new_task = Task(task=task_detail, deadline=deadline)
        return new_task

    def display(self, tasks=None):
        print(self.success, end='\n\n')

    def execute(self, session):
        new_task = self.get_data()
        session.add(new_task)
        session.commit()
        self.display()
        return self.stop


class ExitTask(MenuItem):
    name = 'Exit'
    task_number = EXIT
    stop = True

    def display(self, tasks=None):
        print("\nBye!")

    def execute(self, session):
        self.display()
        return self.stop