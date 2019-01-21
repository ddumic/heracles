import sys
import psutil
import time
import socket
import datetime

sys.path.append('configuration')  
sys.path.append('log')
sys.path.append('shipper')

from elasticshipper import *
from configuration import *
from writer import *

textwriter = writer()

def getService(name):
    service = None
        
    try:
        service = psutil.win_service_get(name)
        service = service.as_dict()
    except Exception as ex:
        textwriter.write('Exception: {}'.format(str(ex)))
        
    return service
        

def services():
    services = configuration.getServices()

    responses = []

    for service in services:
        s = getService(service.value)
        if s and s['status'] == 'running':
            responses.append({'hostname': socket.gethostname(), 'servicename': service.value})

    if configuration.shipToElasticsearch():
                
        hosts = configuration.getElasticHosts()
        ports = configuration.getElasticPorts()
        dateAsId = datetime.datetime.now()

        for x in range(0, len(hosts)):
            elastic = elasticshipper(hosts[x].value, ports[x].value)
            elastic.send('hercules-servicebeat', responses, dateAsId)

if __name__ == "__main__":
        configuration = Configuration()
        interval = configuration.getInterval().value

        while True:
            services()
            textwriter.write('waiting for interval')
            time.sleep(float(interval))

    


