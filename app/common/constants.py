# -*- coding: utf-8 -*-
import sys,os

class RequestMapping(object):
    submit_fetch_url_task = r'/sfut'
    get_current_fetch_worker_queue_opacity = r'/inqopt'
    get_current_fetch_worker_queue_num = r'/inqn'