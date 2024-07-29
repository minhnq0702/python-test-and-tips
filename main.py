# -*- coding: utf-8 -*-
# Copyright MingNe (https://my.mingne.dev/)
import asyncio
import logging
import random
import time

logging.basicConfig(
    level=logging.INFO,  # Mức độ log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
_logger = logging.getLogger(__name__)
FileOutputHandler = logging.FileHandler('output.log')
FileOutputHandler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
_logger.addHandler(FileOutputHandler)


async def async_task_1(name: str = '', _sleep: int = 0):
    """Run long run async task

    Args:
        name (str): task name
        _sleep (int, optional): sleep time (demonstrate a long run task). Defaults to 0.
    """    
    _logger.info(f'Async task {name}....')
    await asyncio.sleep(_sleep) # ! This is a long run task
    _logger.info(f'Complete async task {name}....at timeout {_sleep}')


task_list = []
async def create_task(i: int):
    # await asyncio.create_task(async_task_1(str(i), random.choice(range(10))))
    # await async_task_1(str(i), random.choice(range(10)))
    _logger.info('create complete')
    return asyncio.ensure_future(async_task_1(str(i), random.choice(range(1))))


async def doing_tasks():

    # for i in range(20):
    #     print(f'adding...{i + 1}')
    #     task_list.append(asyncio.create_task(
    #         async_task_1(str(i + 1))
    #     ))
    #     print(f'Done add...')
    # print('Cai gi day')
    await asyncio.gather(*task_list)

async def sleep(sleep_time: int = 5):
    await asyncio.sleep(sleep_time)

if __name__ == '__main__':
    # loop = asyncio.get_event_loop()
    # asyncio.set_event_loop(loop)
    task_list = [create_task(i) for i in range(20)]
    _logger.info(f'Start doing {len(task_list)} tasks....')
    asyncio.run(doing_tasks())
    asyncio.run(sleep())
    _logger.info('Next command....')

