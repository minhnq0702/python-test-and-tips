# pylint: skip-file
import threading
from typing import Callable

lock = threading.Lock()

class Foo:
    def __init__(self):
        self.first_lock = threading.Lock()
        self.second_lock = threading.Lock()
        self.first_lock.acquire()
        self.second_lock.acquire()

    def first(self, printFirst: 'Callable[[], None]') -> None:
        # printFirst() outputs "first". Do not change or remove this line.
        printFirst()
        self.first_lock.release()

    def second(self, printSecond: 'Callable[[], None]') -> None:
        with self.first_lock:
        # printSecond() outputs "second". Do not change or remove this line.
            printSecond()
            self.second_lock.release()

    def third(self, printThird: 'Callable[[], None]') -> None:
        with self.second_lock:
            # printThird() outputs "third". Do not change or remove this line.
            printThird()

obj = Foo()

t1 = threading.Thread(target=obj.first, args=(lambda: print("first"),))
t2 = threading.Thread(target=obj.second, args=(lambda: print("second"),))
t3 = threading.Thread(target=obj.third, args=(lambda: print("third"),))
t3.start()
t1.start()
t2.start()
t3.join()
t1.join()
t2.join()

