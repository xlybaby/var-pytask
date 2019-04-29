# -*- coding: utf-8 -*-
import sys,os

class ApplicationContext(object):
    
    __context = None
    
    class __contx(object):
        def __init__(self):
            self.__pool = {}

        def getInstance(self, p_name):
            return self.__pool[p_name] if p_name in self.__pool else None
        
        def putInstance(self, p_name, p_obj=None):
            self.__pool[p_name] = p_obj
        
    @staticmethod
    def getContext():
        if ApplicationContext.__context is None:
            ApplicationContext.__context = ApplicationContext.__contx()
            
        return ApplicationContext.__context
            
    
        