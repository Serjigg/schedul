import multiprocessing
from job import Job
from tests import *
import time
import uuid
import datetime
from queue import Queue
import threading
import sys

import multiprocessing
import time
import uuid
import datetime
import threading

from utils_sched import check_executed, run_task, kill_old_tasks


class MyScheduler:
    """ планировщик задач как работает:
        - если передаёшь type_run: every_minute -> запускается каждую минуту
        - если передавать minutes = 1 будет запускать каждый час в 1 минуту
        - если передавать hour = 1 minutes = 1 будет запускать каждый день в 1 час в 1 минуту


        """
    def __init__(self):
        self.list_tasks_for_run: list[Job] = []
        self.last_execution_time = {}
        self.time_last_execute = datetime.datetime.now()
        self.lock = threading.Lock()
        self.status_cycle = True
    def run_job(self, job, time_out_collection=9):
        job.link_process.start()

    def get_jobs(self):
        print(self.list_tasks_for_run)
        return self.list_tasks_for_run

    def run_schedule(self):
        time_current = datetime.datetime.now()
        print(time_current, '#' * 50, self.time_last_execute)
        kill_old_tasks(list_task_sched=self.list_tasks_for_run, time_current=time_current)
        run_task(time_current=time_current, time_last_execute=self.time_last_execute,
                 list_task_sched=self.list_tasks_for_run,)
        check_executed(self.list_tasks_for_run)
        self.time_last_execute = datetime.datetime.now()
        time.sleep(1)


    def add_job(self, function_name, type_run, hour=None, minute=None, args='', id=str(uuid.uuid4())):
        job = Job(function=function_name, type_run=type_run, hour=hour, minute=minute, args=args, )
        self.list_tasks_for_run.append(job)
        self.last_execution_time[job.id_task] = datetime.datetime.now().date() - datetime.timedelta(days=1)

    def stop_cycle(self):
        self.status_cycle = False

    def start_cycle(self):
        self.status_cycle = True
        self.cycle_scheduler()

    def remove_job(self, job_id):
        for task in self.list_tasks_for_run:
            if task.id_task == job_id:
                self.list_tasks_for_run.remove(task)
                break


    def cycle_scheduler(self):
        print('start schedul')
        while self.status_cycle:
            self.run_schedule()



def main():
    schedule = MyScheduler()

    # schedule.add_job(function_name=print_hello2, type_run="every_minute",
    #                  args='функция запустилась')
    # schedule.add_job(function_name=print_hello2, type_run="every_minute",
    #                  args='функция2 запустилась')
    schedule.add_job(function_name=print_hello2, type_run="every_day", hour=13, minute=12, args='каждый день1 ')
    schedule.add_job(function_name=print_hello2, type_run="every_day", hour=13, minute=12, args='каждый день 2 задача')
    schedule.add_job(function_name=print_hello2, type_run="every_hour",         minute=12, args='каждый час1')
    schedule.add_job(function_name=print_hello2, type_run="every_hour",         minute=12, args='каждый час2 ')
    schedule.add_job(function_name=print_hello2, type_run="every_minute",  args='каждую минуту ')
    schedule_thread = threading.Thread(target=schedule.cycle_scheduler)
    schedule_thread.start()
    for i in schedule.get_jobs():
        print(i.info_task())

main()
