# -*- coding: utf-8 -*-
import sys,os,json
import tornado.web

from app.context.initializedInstancePool import ApplicationContext
from app.common.constants import RequestMapping

class FectchWorderQueueOpacity(tornado.web.RequestHandler):
    def get(self):
        #print(ApplicationContext.getContext().getInstance( p_name='var.application.inq').qsize())
        self.write({'fetch_queue_opacity':ApplicationContext.getContext().getInstance( p_name='var.application.inq').qsize()})

class FectchWorderQueueNum(tornado.web.RequestHandler):
    def get(self):
        #print(ApplicationContext.getContext().getInstance( p_name='var.application.inq').maxsize)
        self.write({'fetch_queue_maxsize':ApplicationContext.getContext().getInstance( p_name='var.application.inq').maxsize})
    
class dashboard(object):
    
    @staticmethod
    def populate():
        list = []
        list.append((RequestMapping.get_current_fetch_worker_queue_opacity, FectchWorderQueueOpacity))
        list.append((RequestMapping.get_current_fetch_worker_queue_num, FectchWorderQueueNum))
        return list