import sys
sys.path.append('...configuration')

from configuration import *

class writer(object):

    def path(self):
        configuration = Configuration()
        return configuration.getLogPath().value


    def write(self, text):
        path = '{}/{}'.format(self.path(), 'healthbeat.txt')
        
        file = open(path,"a") 
        file.write('{}\n'.format(text))
        file.close() 