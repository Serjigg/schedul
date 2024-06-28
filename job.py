import threading
import uuid
import multiprocessing


class Job:
    def __init__(self, function, hour, minute, type_run,run_cycle = False,time_out=2, args=''):
        self.function = function
        self.hour = hour
        self.minute = minute
        self.args = args
        self.id = str(uuid.uuid4())
        self.link_process = multiprocessing.Process(target=function)
        self.stop_event = threading.Event()
        self.type_run = type_run
        self.status = 'no_active'
        self.time_start = None
        self.time_out = time_out
        self.run_cycle = run_cycle

    def info_task(self):
        return {'function': self.function,
                'hour': self.hour,
                'minutes': self.minute,
                'id': self.id,
                'link_thread': self.link_thread,
                'last_execution': self.time_start,
                'status': self.status}