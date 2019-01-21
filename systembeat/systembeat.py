import sys
import time
import psutil
import socket
import datetime

sys.path.append('configuration')  
sys.path.append('log')
sys.path.append('shipper')

from configuration import *
from writer import *
from elasticshipper import *

textwriter = writer()

pnic_before = psutil.net_io_counters(pernic=True)['Ethernet']

def measureMetrics(metrics):
    responses = []

    network_stats = psutil.net_io_counters(pernic=True)['Ethernet']

    switcher = {
        'cpu': responses.append({'hostname': socket.gethostname(), 'cpu': psutil.cpu_percent()}),
        'memory': responses.append({'hostname': socket.gethostname(), 'memory': psutil.virtual_memory().percent}),
        'disksize': responses.append({'hostname': socket.gethostname(), 'disksize': round(float(psutil.disk_usage("/").total) / 1024 / 1024 / 1024, 2)}),
        'diskused': responses.append({'hostname': socket.gethostname(), 'diskused': round(float(psutil.disk_usage("/").used) / 1024 / 1024 / 1024, 2)}),
        'diskfree': responses.append({'hostname': socket.gethostname(), 'diskfree': round(float(psutil.disk_usage("/").free) / 1024 / 1024 / 1024, 2)}),
        'inboundtraffic': responses.append({'hostname': socket.gethostname(), 'inboundtraffic': round(float((network_stats.bytes_recv - pnic_before.bytes_recv) / 1024), 2)}),
        'outboundtraffic': responses.append({'hostname': socket.gethostname(), 'outboundtraffic': round(float((network_stats.bytes_sent - pnic_before.bytes_sent) / 1024), 2)})
    }

    for metric in metrics:
        switcher.get(metric)

    if configuration.shipToElasticsearch():
                
        hosts = configuration.getElasticHosts()
        ports = configuration.getElasticPorts()
        dateAsId = datetime.datetime.now()

        for x in range(0, len(hosts)):
            elastic = elasticshipper(hosts[x].value, ports[x].value)
            elastic.send('hercules-systembeat', responses, dateAsId)
    

if __name__ == "__main__":
    configuration = Configuration()
    interval = configuration.getInterval().value
    while True:
        metrics = configuration.getMetrics()
        measureMetrics(metrics)
        pnic_before = psutil.net_io_counters(pernic=True)['Ethernet']
        textwriter.write('waiting for interval')
        time.sleep(float(interval))