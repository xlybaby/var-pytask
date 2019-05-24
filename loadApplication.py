# -*- coding: utf-8 -*-
import sys,os,json,codecs
import time
import datetime

import urllib3
import urllib3.contrib.pyopenssl
import certifi

import tornado.ioloop
import tornado.web
from tornado import gen, httpclient, ioloop, queues

from app.init.fileBasedConfiguration import ApplicationProperties
from app.context.initializedInstancePool import ApplicationContext
from app.common.constants import RequestMapping
from module.console.dashboard import dashboard

inq = queues.Queue()

async def async_fetch_https(url,scenarioId,idx):
    print('[%s] async_fetch_https | worker[%d] | scenario[%s] | url[%s]'%(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), idx, scenarioId, url))    
    header = {
        #"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36"
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) VAR/1.0.0.1"
    }
    props = ApplicationContext.getContext().getInstance( p_name='var.application.configuration' )
    datadir = props.getProperty(p_key='application.persistence.rootdir')
    http_client = httpclient.AsyncHTTPClient()
    try:
        response = await http_client.fetch(url,method='GET',headers=header)
    except Exception as e:
        print("Error: %s" % e)
    else:
        fp = open(datadir+"/"+scenarioId, 'wb+')
        fp.write(response.body)
        
async def fetch_https(url,scenarioId,idx):
    #if scenarioId == 'sid-003' or scenarioId == 'sid-007' or scenarioId == 'sid-0013' or scenarioId == 'sid-0016':
     #   await gen.sleep(15)
    
    print('[%s] fetch_https | worker[%d] | scenario[%s] | url[%s]'%(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), idx, scenarioId, url))    
    header = {
        #"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36"
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) VAR/1.0.0.1"
    }
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
    response = http.request('GET', url, None, header)
    #data = response.data.decode('utf-8') # 注意, 返回的是字节数据.需要转码.
    #print (data) # 打印网页的内容
    props = ApplicationContext.getContext().getInstance( p_name='var.application.configuration' )
    datadir = props.getProperty(p_key='application.persistence.rootdir')
    if url == 'http://www.160ys.com/forum-39-1.html':
        fp = codecs.open(datadir+"/"+scenarioId, 'w+', encoding='gbk')
        data = response.data.decode('gbk')
        #print(data.encode('latin-1').decode('gbk').encode('utf-8'))
        fp.write(data)
        fp.close()
    else:
        fp = open(datadir+"/"+scenarioId, 'wb+')
        fp.write(response.data)

async def worker(idx):
    async for task in inq:
                    url = task['url']
                    scenarioId  = task['scenarioId']
                    if url is None:
                        return
                    try:
                        #await fetch_url(p_url=url)
                        #print('worker-%d begin fetch url(%s) - %s'%(idx, url, datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                        #await gen.sleep(5)
                        #await fetch_https(url,scenarioId,idx)
                        await async_fetch_https(url,scenarioId,idx)
                        print('[%s] fetch_https ends | worker[%d] | scenario[%s] | url[%s]'%(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), idx, scenarioId, url))    

                        #print('worker-%d end fetch url - %s'%(idx,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
                    except Exception as e:
                        print("Exception: %s %s" % (e, url))
                    finally:
                        inq.task_done()

class dashboard(tornado.web.RequestHandler):
    async def get(self):
        qsize = inq.qsize();
        self.write({'fetch_queue_opacity':qsize})
        
class MainHandler(tornado.web.RequestHandler):
    def prepare(self):
        if 'Content-Type' not in self.request.headers:
            raise Exception('Unsupported content-type!')
         
        if  self.request.headers['Content-Type'].strip().startswith('application/json'):
            self.args = json.loads(self.request.body)
        else:
            raise Exception('Unsupported content-type!',self.request.headers['Content-Type'])

    async def post(self):
        #request = ApplicationContext.getContext().getInstance( p_name='var.application.urlRequest')
        #print('reqeust incoming...%s'%(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        await inq.put(self.args);
        print('[%s] -- put message into queue'%(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        self.write('Gotta')
        
def Main(p_command=None):        
        properties = ApplicationProperties(p_command)
        #dlist = dashboard.populate() + [ (RequestMapping.submit_fetch_url_task, MainHandler)]
        application = tornado.web.Application([ (RequestMapping.submit_fetch_url_task, MainHandler),
                                                                                   (RequestMapping.get_current_fetch_worker_queue_num, dashboard), ])
        application.listen(properties.getProperty(p_key='server.port'))
        
        workers = gen.multi([worker(idx) for idx in range(int(properties.getProperty(p_key='application.worker.fetchUrl.num')))])
        ioLoop = tornado.ioloop.IOLoop.current()

        #request = HttpRequest()
        #await request.do()
        #ApplicationContext.getContext().putInstance( p_name='var.application.inq', p_obj=inq )
        ApplicationContext.getContext().putInstance( p_name='var.application.workers', p_obj=workers )
        ApplicationContext.getContext().putInstance( p_name='var.application.configuration', p_obj=properties )
        ApplicationContext.getContext().putInstance( p_name='var.application.webApplication', p_obj=application )
        #ApplicationContext.getContext().putInstance( p_name='var.application.urlRequest', p_obj=request )
        ApplicationContext.getContext().putInstance( p_name='var.ioloop.current', p_obj=ioLoop )
        ioLoop.start()
        #ioLoop.run_sync()
 
if __name__ == '__main__':
    urllib3.contrib.pyopenssl.inject_into_urllib3()

    props={}
    if len(sys.argv) > 1:
        for idx in range(1, len(sys.argv)):
            arg = sys.argv[idx]
            if arg.startswith("--") :
                prop = arg[2:]
                pair = prop.split("=")
                props[pair[0]]=pair[1]
                print ("command props", props)
                
    #io_loop = tornado.ioloop.IOLoop.current()
    #io_loop.run_sync(Main)     
    Main()