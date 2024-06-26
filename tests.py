import datetime
import time


def print_hello(text):
    time.sleep(10)
    print('Hello world', text)

def print_hello2():
    print('Hello world2', time.time_ns(), '    ', datetime.datetime.now())

def print_hello3(text):
    print('Hello world3', time.time_ns(), '    ', datetime.datetime.now(),  text)