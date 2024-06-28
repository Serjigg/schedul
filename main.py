import multiprocessing

from job import Job
import time
import uuid
import datetime
from queue import Queue
import threading
import stopit
from typing import Literal
import sys
from  tests import *

# def print_hello():
#     for i in range(10):
#         print(f'работаю {i}')
#         time.sleep(1)
#     print('завершилась')
#
# def print_hello2():
#     print('Hello world2', time.time_ns(), '    ', datetime.datetime.now())
#
# def print_hello3():
#     print('Hello world3', time.time_ns(), '    ', datetime.datetime.now())

class MyScheduler:
    TaskType = Literal['every_minute', 'every_hour', 'every_day', 'once']

    def __init__(self):
        self.list_tasks_for_run: list[Job] = []
        self.last_execution_time = {}
        self.time_last_execute = datetime.datetime.now()
        self.lock = threading.Lock()

    def run_job(self, job, time_out_collection=9):
        job.link_process.start()

    def run_schedule(self):
        time_current = datetime.datetime.now()
        print(time_current, '#' * 50, self.time_last_execute)
        try:
            for task in self.list_tasks_for_run:
                if task.time_start is not None and ((time_current - task.time_start).total_seconds()) >= task.time_out:
                    if task.link_process.is_alive():
                        task.link_process.terminate()
                        task.link_process.kill()
                    task = None

            if self.time_last_execute.minute != time_current.minute:
                print('new_minute')
                list_tasks_every_minute = list(
                    filter(lambda task: task.type_run == 'every_minute', self.list_tasks_for_run))
                for task in list_tasks_every_minute:
                    if not task.link_process.is_alive():
                        t = multiprocessing.Process(target=task.function, args=(task.args,))
                        t.start()
                        task.link_process = t
                        task.time_start = datetime.datetime.now()

            if self.time_last_execute.hour != time_current.hour:
                print('new_hour')
                list_tasks_every_hour = list(filter(lambda task: task.type_run == 'every_hour', self.list_tasks_for_run))
                for task in list_tasks_every_hour:
                    if task.minute == time_current.minute:
                        if not task.link_process.is_alive():
                            t = multiprocessing.Process(target=task.function)
                            t.start()
                            task.link_process = t
                            task.time_start = datetime.datetime.now()
            if self.time_last_execute.hour != time_current.hour:
                print('new_hour')
                list_tasks_every_hour = list(filter(lambda task: task.type_run == 'every_hour', self.list_tasks_for_run))
                for task in list_tasks_every_hour:
                    if task.minute == time_current.minute:
                        if not task.link_process.is_alive():
                            t = multiprocessing.Process(target=task.function)
                            t.start()
                            task.link_process = t
                            task.time_start = datetime.datetime.now()
            self.time_last_execute = datetime.datetime.now()
            time.sleep(1)
        except Exception as a:
            print(a)

    def add_job(self, function_name, type_run, hour=0, minute=0, args=''):
        job = Job(function=function_name, type_run=type_run, hour=hour, minute=minute, args=args)
        self.list_tasks_for_run.append(job)
        self.last_execution_time[job.id] = datetime.datetime.now().date() - datetime.timedelta(days=1)

    def cycle_scheduler(self):
        print('start schedul')
        while True:
            self.run_schedule()

def main():
    schedule = MyScheduler()
    schedule.add_job(function_name=print_hello, type_run="every_minute", args='каждую минуту')
    #schedule.add_job(function_name=print_hello, minute=1, type_run="every_hour", args='каждый час5')
    #schedule.add_job(function_name=print_hello3, hour=7, minute=50, type_run="every_day", args='каждый день')
    schedule_thread = threading.Thread(target=schedule.cycle_scheduler)
   # schedule_thread = multiprocessing.Process(target=schedule.cycle_scheduler)
    schedule_thread.start()

main()
# if __name__ == '__main__':
#     schedule = MyScheduler()
#
#
#     schedule.add_job(function_name=print_hello, type_run="every_minute", args='1 task')
#     schedule.add_job(function_name=print_hello, type_run="every_minute", args='2 task')
#     schedule.add_job(function_name=print_hello, minute=30, type_run="every_hour", args='каждый час 3 задача')
#     # schedule.add_job(function_name=print_hello3, hour=7, minute=50, type_run="every_day", args='каждый день')
#     schedule_thread = threading.Thread(target=schedule.cycle_scheduler)
#     # schedule_thread = multiprocessing.Process(target=schedule.cycle_scheduler)
#     schedule_thread.start()