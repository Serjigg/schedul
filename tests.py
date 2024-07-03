import time
import datetime
def print_hello(a):
    print(a)
    for i in range(10):
        print(f'работаю {i}')
        time.sleep(1)
    print('завершилась')

def print_hello2(a):
    print('Hello world2', time.time_ns(), '    ', datetime.datetime.now(), a)

def print_hello3():
    print('Hello world3', time.time_ns(), '    ', datetime.datetime.now())