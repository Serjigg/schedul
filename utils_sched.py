import datetime
import multiprocessing

def kill_old_tasks(list_task_sched, time_current):
    for task in list_task_sched:
        if task.time_start is not None and ((time_current - task.time_start).total_seconds()) >= task.time_out:
            if task.link_process.is_alive():
                task.link_process.terminate()
                task.link_process.kill()

def check_executed(list_task_sched):
    list_tasks_every_minute = list(filter(lambda task: task.status_run == 'executed', list_task_sched))
    for task in list_tasks_every_minute:
        if (datetime.datetime.now() - task.time_start).total_seconds() >= 60:
            if task.link_process.is_alive():
                continue
            else:
                task.status_run = 'not executed'

def run_task(time_last_execute, time_current, list_task_sched):
    if time_current.minute != time_last_execute.minute:
        list_tasks_every_minute = list(
            filter(lambda task: task.type_run == 'every_minute', list_task_sched))
        for task in list_tasks_every_minute:
            if not task.link_process.is_alive() and task.time_start is None and task.status_run == 'not executed':
                t = multiprocessing.Process(target=task.function, args=(task.args,))
                t.start()
                task.link_process = t
                task.status_run = 'executed'

                task.time_start = datetime.datetime.now()

        for task in list_task_sched:
            if task.day == time_current.day and task.hour == time_current.hour and task.minute == time_current.minute:
                if not task.link_process.is_alive() and  task.time_start is None and task.status_run == 'not executed':
                    t = multiprocessing.Process(target=task.function, args=(task.args,))
                    t.start()
                    task.link_process = t
                    task.status_run = 'executed'
                    task.time_start = datetime.datetime.now()

            if task.day is None and task.hour == time_current.hour and task.minute == time_current.minute:
                if not task.link_process.is_alive() and  task.time_start is None and task.status_run == 'not executed':
                    t = multiprocessing.Process(target=task.function, args=(task.args,))
                    t.start()
                    task.link_process = t
                    task.status_run = 'executed'

                    task.time_start = datetime.datetime.now()

            #    ' every hour'

            if task.day is None and task.hour is None and task.minute == time_current.minute:

                if not task.link_process.is_alive() and  task.time_start is None and task.status_run == 'not executed':
                    t = multiprocessing.Process(target=task.function, args=(task.args,))
                    t.start()
                    task.link_process = t
                    task.status_run = 'executed'
                    task.time_start = datetime.datetime.now()


            #    ' every minutes'
            if task.day is None and task.hour is None and task.minute is None:
                print('каждую минуту')
