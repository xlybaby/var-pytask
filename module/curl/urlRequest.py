# -*- coding: utf-8 -*-
import sys,os
import time
from datetime import timedelta

from html.parser import HTMLParser
from urllib.parse import urljoin, urldefrag

from tornado import gen, httpclient, ioloop, queues

async def fetch_url(p_url):
    print('Got on url: %s'%(p_url))
    
class HttpRequest(object):
    
    def __init__(self):
        self.__q = queues.Queue()
        #self.do()
        async def worker():
            async for url in self.__q:
                if url is None:
                    return
                try:
                    await fetch_url(p_url=url)
                except Exception as e:
                    print("Exception: %s %s" % (e, url))
                finally:
                    self.__q.task_done()
    
        # Start workers, then wait for the work queue to be empty.
        self.__workers = gen.multi([worker() for _ in range(10)])
        
    def getQueue(self):
        return self.__q
    
    async def put(self, p_url):
        await self.__q.put(p_url)

        
       