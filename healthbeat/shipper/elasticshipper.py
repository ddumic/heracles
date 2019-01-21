import sys
import json

sys.path.append('log')

from elasticsearch import Elasticsearch
from writer import *

class elasticshipper(object):
    host = ''
    port = ''

    writer = writer()

    def __init__(self, host, port):
        self.host = host
        self.port = port

    def send(self, indices, data, identifier):
        es = Elasticsearch([{'host': self.host,'port': self.port}])

        hosttext = '{}:{}'.format(self.host, self.port)
        self.writer.write('{} {} {} {}'.format('sending data', json.dumps({'data': data}), 'to', hosttext))

        res = es.index(index=indices, doc_type='Hhealthbeat', id=identifier, body=json.dumps({'data': data}))
        self.writer.write('data sent to {}:{}'.format(self.host, self.port))