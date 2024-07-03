import threading
import uuid
import multiprocessing


class Job:
    def __init__(self, function, type_run, hour=None, minute=None, day=None, run_cycle=False, time_out=2, args='',
                 id_task=None):
        self.function = function
        self.args = args
        self.day = day
        self.hour = hour
        self.minute = minute
        self.time_out = time_out
        self.type_run = type_run
        self.link_process = multiprocessing.Process(target=self.function, args=(self.args,))
        self.time_start = None
        self.status_run = 'not executed'
        self.id_task = id_task

    def info_task(self):
        return {'function': self.function,
                'hour': self.hour,
                'minutes': self.minute,
                'day': self.day,
                'time_start': self.time_start,
                'id': self.id_task,
                'status_run': self.status_run}