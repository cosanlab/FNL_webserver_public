"""
Call by creating a copy of the class (i.e. >>> n = Data_Pull_Class(<args>)), then run by calling n.get()
The get function can take the same arguments as __init__
"""



import requests
import os

basedir = '/home/cosanlab/tv.cosanlab.com'
# basedir = '/Users/Strotifiler/Dropbox/Clean/'

import imp
keypath = imp.load_source('keys', os.path.join(basedir,'keys','keys.py'))
keys = keypath.Keys()

api_key = keys.api_key

"Hierarchy option for API:"
"tv.cosanlab.com/api/<study>/<dataset>/?key=<key>&<query>"

"Current hierarchy (exclusively for the tv study/subtitles)"
"tv.cosanlab.com/api/<study>/<episode>/?key=<key>&<query>"

class Data_Pull_Class():
    def __init__(self, study, episode, args):
        #args to parse is a tuple of dictionaries, each corresponding to a different call
        self.study = study
        self.episode = episode

        if type(args) != tuple:
            args = (args,)
        self.args = args

        self.n = 1
        self.URLs = []
        if self.args == None:
            self.parsed_args = '?key=%s'%api_key
            self.URLs.append('http://tv.cosanlab.com/api/%s/%s/%s'%(self.study, self.episode, self.parsed_args))
        else:
            self.parsed_args = '?key=%s&'%api_key
            for arg in self.args:
                for key in arg:
                    if self.n < len(arg):
                        self.parsed_args += '%s=%s&'%(key, arg[key])
                        self.n += 1
                    else:
                        self.parsed_args += '%s=%s'%(key, arg[key])
                self.URLs.append('http://tv.cosanlab.com/api/%s/%s/%s'%(self.study, self.episode, self.parsed_args))
                self.parsed_args='?key=%s&'%api_key
                self.n = 1

    def get(self, study=None, episode=None, args=None):
        if study != None:
            if study != self.study:
                self.study = study
        if episode != None:
            if episode != self.episode:
                self.episode = episode
        if args != None:
            if args != self.args:
                self.args = args
        if study == None and episode == None and args == None:
            self.data = ''
            for URL in self.URLs:
                self.data += '%s\n'%requests.get(URL).text
            self.data = self.data.replace('\\n','')
            return self.data
        else:
            self.__init__(self.study, self.episode, self.args)
            self.data = ''
            for URL in self.URLs:
                self.data += '%s\n'%requests.get(URL).text
            self.data = self.data.replace('\\n','')
            return self.data


# "Testing the query"

# def data_pull_demo():
#     args = ({'start':'00:00:00', 'end':'00:00:10'},{'start':'00:10:00', 'end':'00:10:10'},{'start':'00:20:00', 'end':'00:20:10'})
#     n = Data_Pull_Class('FNL','ep2',args)
#     return n

# def demo():
#     n = data_pull_demo()
#     print n.get('FNL','ep1',({'start':'00:10:00', 'end':'00:10:10'},{'start':'00:00:00', 'end':'00:00:10'}))
#     return n

# n = demo()