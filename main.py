import queue
import sched
import time
import asyncio
import threading


def thread_event():
    print('This is thread event\n')
    time.sleep(2)
    # asyncio.sleep(2)
    print('Thread Event 1 completed/1\n')
    time.sleep(2)
    # asyncio.sleep(2)
    print('Thread Event 1 completed/2\n')
    time.sleep(2)
    # asyncio.sleep(2)
    print('Thread Event 1 completed\n')


def thread_event2():
    print('This is thread event 2\n')
    time.sleep(5)
    # asyncio.sleep(5)
    print('Thread Event 2 completed\n')


def thread_task(func):
    print('This is thread task')
    func()


def make_thread():
    # INIT new thread
    thread1 = threading.Thread(target=thread_task, args=[thread_event])
    thread2 = threading.Thread(target=thread_task, args=[thread_event2])
    # thread.daemon = True
    thread1.start()
    thread2.start()
    for th in [thread1, thread2]:
        print('join thread', th)
        th.join()

    print('Do another thing')
    print('end')
    return 'exit thread'


# if __name__ == '__main__':
#     res = make_thread()
#     print(f'Xử lý luồng main')


global_list = []
global_q = queue.Queue()

async def async_event():
    for i in range(20000):
        # await asyncio.sleep(0.006)
        global_list.append({
            'id': i,
            'state': 'done',
        })
        print('event1')


async def async_event2():
    for i in range(20000):
        # await asyncio.sleep(0.2)
        global_list.append(i)
        # print('event2', global_list)


async def _manager():
    tasks = []
    for i in [async_event, async_event, async_event, async_event, async_event, async_event]:
        test = asyncio.create_task(i())
        tasks.append(test)

    for t in tasks:
        print('await', t)
        await t
        print('complete', t)

    # while True:
    #     global_list.append(global_q.get())
    #     if global_q.empty():
    #         break

    # funcs = [async_event(), async_event2()]
    # await asyncio.gather(*funcs)

if __name__ == '__main__':
    s = time.time()
    asyncio.run(_manager())
    print(f'Xử lý luồng main {time.time() -s }', len(global_list))


