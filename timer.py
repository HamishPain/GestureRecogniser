__author__ = 'Finch ThinkPad'
from time import clock

def timeDelta():
    time = clock()
    while 1:
        delta = clock()-time
        time = clock()
        yield(delta)