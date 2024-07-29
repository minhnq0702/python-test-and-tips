import asyncio
import concurrent
import concurrent.futures
import logging
import threading
import time

import aiohttp
import requests

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)
_logger = logging.getLogger(__name__)

data_to_process = ['https://dummyjson.com/products?limit=10']
MAX_CONCURRENT = 10

def new_async_client():
    return aiohttp.ClientSession()

def new_client():
    return requests.Session()


def fetch_datas_sequential(urls: list):
    start = time.time()
    client = new_client()
    for url in urls:
        response = client.get(url)
    _logger.info(f'Fetch data sequentially done in {time.time() - start} seconds')


thread_local = threading.local()
def get_client():
    if not hasattr(thread_local, 'client'):
        thread_local.client = new_client()
    return thread_local.client

def _do_fetch_data_by_thread(url: str) -> str:
    """This fetch will run in each separated thread

    Args:
        url (str): url to fetch data

    Returns:
        str: sample string
    """
    with get_client().get(url) as resp:
        # _logger.info(f'Fetch data by thread done for {resp.status_code}')
        pass
        
        
    return 'success'

def fetch_datas_by_thread(urls: list):
    start = time.time()
    res = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_CONCURRENT) as executor:
        # * 1. use map
        # for r in executor.map(_do_fetch_data_by_thread, urls):
        #     res.append(r)
        

        # * 2. use submit
        for url in urls:
            future = executor.submit(_do_fetch_data_by_thread, url)
            # r = future.result() # ! this will make thread run sequentially
            future.add_done_callback(lambda x: res.append(x.result()))
            
    _logger.info(f'Fetch data by thread done in {time.time() - start} seconds with response {res}')


async def _do_fetch_data_by_async(_client: aiohttp.ClientSession, url: str) -> str:
    async with _client.get(url) as resp:
        # _logger.info(f'Fetch data by async done for {resp.status}')
        pass

    return 'async success'


def fetch_datas_by_async(urls: list):
    start = time.time()
    async def _async_fetch_datas():
        # init client use for all concurrent requests
        async with new_async_client() as client:
            tasks = []
            for url in urls:
                task = asyncio.ensure_future(_do_fetch_data_by_async(client, url))
                tasks.append(task)
            await asyncio.gather(*tasks)
    asyncio.run(_async_fetch_datas())
    

    _logger.info(f'Fetch data by async done in {time.time() - start} seconds')


if __name__ == '__main__':
    multiple_urls = data_to_process * 50

    # Sequential fetching
    # fetch_datas_sequential(multiple_urls)

    # Concurrent Fetching by thread
    # fetch_datas_by_thread(multiple_urls)

    # Concurrent Fetching by async
    fetch_datas_by_async(multiple_urls)
    