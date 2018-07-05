import random

from time import process_time as timer_func, sleep
from contextlib import contextmanager

a1, a2 = [], []

def setup(n):
    global a1, a2
    a1 = random.sample(range(0, 2*n), n)
    a2 = random.sample(range(0, 2*n), n)

contextmanager
def timer():
    try:
        start = timer_func()
        yield
    except Exception as e:
        print(e)
        raise
    finally:
        end = timer_func()
        print('time spent => ', 1000.0* (end - start), 'ms.')


def common_items_v1(seq1, seq2):
    """ Find common items between two sequences - version #1 """

    common = []
    for item in seq1:
        if item in seq2:
            common.append(item)

    return common

def common_items_v2(seq1, seq2):
    """ Find common items between two sequences - optimized version (v2) """

    # return set(seq1).intersection(set(seq2))
    seq_dict1 = {item:1 for item in seq1}
    for item in seq2:
        try:
            seq_dict1[item] += 1
        except KeyError:
            pass

    return [item[0] for item in seq_dict1.items() if item[1]>1]