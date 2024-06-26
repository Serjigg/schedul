from job import Job
import time
import uuid
import datetime
from queue import Queue
import threading


every_minute = 'every minute'
every_hour = 'every hour' #-> minutes
every_day = 'every day' #-> minutes hour
from typing import Literal

def print_hello(text):
    time.sleep(10)
    print('Hello world', text)

def print_hello2():
    print('Hello world2', time.time_ns(), '    ', datetime.datetime.now())

def print_hello3(text):
    print('Hello world3', time.time_ns(), '    ', datetime.datetime.now(),  text)


class MyScheduler:
    TaskType = Literal['every_minute', 'every_hour', 'every_day', 'once']

    def __init__(self):
        self.list_tasks_for_run : list[Job] = []
        self.last_execution_time = {}
        self.task_queue = Queue()
        self.lock = threading.Lock()
        self.time = datetime.datetime.now()

    def run_job(self, job, time_out_collection=9, ):
        def job_wrapper():
            try:
                start_time = time.time()
                job.function(job.args)
                end_time = time.time()
                if end_time - start_time > time_out_collection:
                    job.stop_event.set()
                    # TODO Удалять задачу
                    print(f"Task {job.id} exceeded {time_out_collection} seconds, terminating thread.")
            except Exception as e:
                print(f"Error in task {job.id}: {e}")
                job.stop_event.set()

        job_thread = threading.Thread(target=job_wrapper)
        job_thread.start()
        job_thread.join(timeout=time_out_collection, )
        if job_thread.is_alive():
            job.stop_event.set()
            print(f"Job {job.id} вышло время.")
            # if job.stop_event.is_set():
            #     print(f"Task {job.id} has stopped")

        #print(f"Task {job.id} terminated due to timeout.")

    def run_schedule(self):
        current_time = datetime.datetime.now()
        if self.time.minute != current_time.minute:
            task_every_minute = list(filter(lambda task: task.type_run == 'every_minute', self.list_tasks_for_run))
            for job in task_every_minute:
                job.link_thread = threading.Thread(target=self.run_job, args=(job,))
                job.status = 'active'
                job.link_thread.start()
                job.last_execution = datetime.datetime.now()
                if job.link_thread is not None and not job.link_thread.is_alive():
                    job.status = 'no_active'
            self.time = self.time.replace(minute=current_time.minute)


        if self.time.hour != current_time.hour:
            task_every_hour = list(filter(lambda task: task.type_run == 'every_hour', self.list_tasks_for_run))
            for job in task_every_hour:
                if job.minute == self.time.minute:
                    job.link_thread = threading.Thread(target=self.run_job, args=(job,))
                    job.status = 'active'
                    job.link_thread.start()
                    job.last_execution = datetime.datetime.now()
                    if job.link_thread is not None and not job.link_thread.is_alive():
                        job.status = 'no_active'
            self.time = self.time.replace(minute=current_time.hour)
            # x = job.info_task()
            # time.sleep(0.5)
            # print(x)
            # print('#'*230,datetime.datetime.now())



        if self.time.day != current_time.day:
            task_every_day = list(filter(lambda task: task.type_run == 'every_day', self.list_tasks_for_run))


    def add_job(self, function: object, type_run, hour=0, minute=0, args='', ):
        with self.lock:
            job = Job(function=function,type_run=type_run,hour=hour, minute=minute, args=args)
            self.list_tasks_for_run.append(job)
            self.last_execution_time[job.id] = datetime.datetime.now().date() - datetime.timedelta(days=1)

    def cycle_scheduler(self):
        while True:
            self.run_schedule()

def main():

    schedule = MyScheduler()
    schedule.add_job(function=print_hello3,          minute=1, type_run="every_hour", args='каждый час')
    #schedule.add_job(function=print_hello3,          type_run="every_minute", args='каждую минуту')
    schedule.add_job(function=print_hello3,          minute=11, type_run="every_hour", args='каждую час')
   # schedule.add_job(function=print_hello3, hour=10, minute=45, type_run="every_day", args='каждый день')

    schedule_thread = threading.Thread(target=schedule.cycle_scheduler)
    schedule_thread.start()


main()