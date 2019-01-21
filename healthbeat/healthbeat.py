import sys
import time
import socket
import datetime

sys.path.append('http')
sys.path.append('configuration')
sys.path.append('shipper')
sys.path.append('log')

from http import *
from configuration import *
from elasticshipper import *
from writer import *

textwriter = writer()

def heartbeat(url):
        client = HttpClient()
        response = client.get(url)
        return {'endpoint': response.endpoint,'status': response.responseStatus, 'code': response.responseCode, 'hostname': socket.gethostname()}

def urls():
        configuration = Configuration()
        urls = configuration.getUrls()

        responses = []

        for url in urls:
                responses.append(heartbeat(url.value))

        if configuration.shipToElasticsearch():
                
                hosts = configuration.getElasticHosts()
                ports = configuration.getElasticPorts()
                dateAsId = datetime.datetime.now()

                for x in range(0, len(hosts)):
                        elastic = elasticshipper(hosts[x].value, ports[x].value)
                        elastic.send('hercules-healthbeat', responses, dateAsId)

if __name__ == "__main__":
        configuration = Configuration()
        interval = configuration.getInterval().value

        while True:
                urls()
                textwriter.write('waiting for interval')
                time.sleep(float(interval))