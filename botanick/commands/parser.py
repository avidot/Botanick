# -*- coding: UTF-8 -*-

import argparse
import os
from const import BASE_PATH
from const import VERSION

def sample():
  pass

def version():
  print(VERSION)

class Parser():
    """
    Command line parser
    """
    __args = None
    __instance = None
    __command = None
    __binding = {'sample': sample, 'version': version}
    __parser = None
    __subparser = None
    __args = None
    
    def __new__(cls):
        """
        Singleton
        """
        if Parser.__instance is None:
            Parser.__instance = object.__new__(cls)
        return Parser.__instance
    
    def __init__(self):
        """
        Initialize command parser and subcommands
        """
        self.__parser = argparse.ArgumentParser(description="Python command line utilities {0}".format(VERSION))
        self.__subparser = self.__parser.add_subparsers(description='valid subcommands', help='the sub-command to use')
        self.__sample()
        self.__version()
        self.__args = vars(self.__parser.parse_args())
        try:
            self.__command = self.__args['which']
        except KeyError:
            self.__parser.print_help()
            exit(1)
            
    def __sample(self):
        """
        Sample subcommand for your command line application
        """
        start = self.__subparser.add_parser('start', description='Call the sample subcommand')
        start.set_defaults(which='sample')
        start.add_argument('-opt', '--optionnal', help='optionnal argument')
        
    def __version(self):
        """
        Display current version
        """
        version = self.__subparser.add_parser('version', description='Display current version')
        version.set_defaults(which='version')
    
    def getCommand(self):
        """
        Return the selected sub-command
        """
        try:
            return self.__binding[self.__command]
        except KeyError:
            print('Unrecognized command !')
            self.__parser.print_help()
            exit(1)
            
    def getArgs(self):
        """
        Return the args of the selected sub-command
        """
        return {key: value for key, value in self.__args.items() if key != 'which'}
        
