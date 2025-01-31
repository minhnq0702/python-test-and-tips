# -*- coding: utf-8 -*-

from task import hello, hello_next

result = hello.delay()

result2 = hello_next.apply_async(countdown=10)
print('Task result:', result.get(), result2.get())
