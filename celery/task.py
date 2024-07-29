# -*- coding: utf-8 -*-
import logging
from celery import Celery

_logger = logging.getLogger(__name__)

app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')


@app.task(name='tasks.first')
def hello():
    _logger.info('Hello world!')
    return 'hello world'


@app.task(name='tasks.second')
def hello_next():
    _logger.info('Hello next world!')
    return 'hello next world'
