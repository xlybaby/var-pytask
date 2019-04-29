# -*- coding: utf-8 -*-
import sys,os

class ApplicationProperties(object):
    
    def __init__(self, p_command=None):
        self.__properties = {}
        self.__project_path = sys.path[0]
        
        if( os.path.exists( self.__project_path + '/application.properties' ) ):
            file = open(self.__project_path + '/application.properties', 'r')
            for line in file.readlines():
                pair = line.split("=")
                self.__properties[pair[0]] = pair[1].strip('\n\r\t ')
        
        if p_command:
            for item in p_command.items():
                self.__properties[item[0]] = item[1]
            
    def getProperty(self, p_key):
        return self.__properties[p_key] if p_key in self.__properties else None
    
    def list(self):
        for item in self.__properties.items():
            print( "%s=%s" % (item[0], item[1]) )