# -*- coding: utf-8 -*-
# Copyright MingNe (https://my.mingne.dev/)
import json
import logging
import os
import select
import selectors
import threading
import time

import faker

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
_logger = logging.getLogger(__name__)


def spawn_new_worker(write_pipe):
    print('>>>>>>>>>>>>> Starting new worker....')
    def _sub_main():
        pid = os.fork()
        if pid == 0:
            _logger.info(f'Worker PID({pid}) is starting up...')
        else:
            _logger.info('===> %s', pid)
            return
        
        _f = faker.Faker('en_US')
        while True:
            time.sleep(2)
            val = {
                'pid': os.getpid(),
                'name': _f.name(),
                'city': _f.city(),
                'address': _f.address(),
            }
            os.write(write_pipe, json.dumps(val).encode())
            time.sleep(4)
            print('Sub thread running.....')
            val = {
                **val,
                'nexttime': True,
            }
            os.write(write_pipe, json.dumps(val).encode())

    my_thread = threading.Thread(name='SubThread', target=_sub_main)
    my_thread.start()
    


if __name__ == '__main__':
    rp, wp = os.pipe()
    # Start the worker, process data and push it to the pipe
    _logger.info(f'Starting main process....========> {os.getpid()}')
    spawn_new_worker(wp)
    
    sel = selectors.DefaultSelector()
    sel.register(rp, selectors.EVENT_READ)

    while True:
        # print('waiting os...')
        start = time.time()
        _logger.info(f'{os.getpid()} - Starting select....')
        events = sel.select(None) # Blocking for waiting I/O
        _logger.info('Received signal....%s', time.time() - start)
        for key, mask in events:
            if mask & selectors.EVENT_READ:
                data = os.read(key.fd, 1024)
                print("Read data:", data.decode(), mask & selectors.EVENT_READ, selectors.EVENT_READ)
            print('key==>', key)
            print('mask==>', mask)
