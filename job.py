import threading
import uuid


class Job:
    def __init__(self, function, hour, minute, type_run, args=''):
        self.function = function
        self.hour = hour
        self.minute = minute
        self.args = args
        self.id = str(uuid.uuid4())
        self.link_thread = None
        self.stop_event = threading.Event()
        self.type_run = type_run
        self.status = 'no_active'
        self.last_execution = None

    def info_task(self):
        return {'function': self.function,
                'hour': self.hour,
                'minutes': self.minute,
                'id': self.id,
                'link_thread': self.link_thread,
                'last_execution': self.last_execution,
                'status': self.status}