# Write your code here

def display_task(tasks_list):
    print("Today:")
    if tasks_list:
        txt = "{}) {}"
        for i, task in enumerate(tasks_list, start=1):
            print(txt.format(i, task))
    else:
        print("Nothing to do!")


if __name__ == '__main__':
    tasks = ['Do yoga', 'Make breakfast', 'Learn basics of SQL', 'Learn what is ORM']
    display_task(tasks)