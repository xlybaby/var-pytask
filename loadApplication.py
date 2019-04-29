# -*- coding: utf-8 -*-
import sys,os
import tornado.ioloop
import tornado.web
from datetime import timedelta

from app.init.fileBasedConfiguration import ApplicationProperties
from app.context.initializedInstancePool import ApplicationContext
from app.common.constants import RequestMapping

from module.curl.urlRequest import HttpRequest
from tornado import gen, httpclient, ioloop, queues

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        request = ApplicationContext.getContext().getInstance( p_name='var.application.urlRequest')
        request.put('http://www.tornadoweb.org/en/stable/');
        
async def Main(p_command=None):        
        properties = ApplicationProperties(p_command)
        application = tornado.web.Application([ (RequestMapping.submit_fetch_url_task, MainHandler),])
        application.listen(properties.getProperty(p_key='server.port'))
        
        request = HttpRequest()
        #await request.do()
        print('http request initialized')
        ApplicationContext.getContext().putInstance( p_name='var.application.configuration', p_obj=properties )
        ApplicationContext.getContext().putInstance( p_name='var.application.webApplication', p_obj=application )
        ApplicationContext.getContext().putInstance( p_name='var.application.urlRequest', p_obj=request )

        #ioLoop = tornado.ioloop.IOLoop.current()
        #ApplicationContext.getContext().putInstance( p_name='var.ioloop.current', p_obj=ioLoop )
       # ioLoop.start()
        #ioLoop.run_sync()
 
if __name__ == '__main__':
    props={}
    if len(sys.argv) > 1:
        for idx in range(1, len(sys.argv)):
            arg = sys.argv[idx]
            if arg.startswith("--") :
                prop = arg[2:]
                pair = prop.split("=")
                props[pair[0]]=pair[1]
                print ("command props", props)
                
    io_loop = tornado.ioloop.IOLoop.current()
    io_loop.run_sync(Main)     
    #Main()