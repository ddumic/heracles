import yaml

class ConfigurationItem(object):
    value = ''

    def __init__(self, value):
        self.value = value


class Configuration(object):
    
    config = yaml.load(open('systembeat.yml'))

    def getMetrics(self):
        configuration = self.config['systembeat.monitors']
        
        metrics = configuration.get('metrics')

        returnValue = []

        if metrics[0] == '*':
            returnValue.append(ConfigurationItem('cpu'))
            returnValue.append(ConfigurationItem('memory'))
            returnValue.append(ConfigurationItem('disksize'))
            returnValue.append(ConfigurationItem('diskused'))
            returnValue.append(ConfigurationItem('diskfree'))
            returnValue.append(ConfigurationItem('inboundtraffic'))
            returnValue.append(ConfigurationItem('outboundtraffic'))
        
        else:
            for metric in metrics:
                returnValue.append(ConfigurationItem(metric))

        return returnValue


    def getInterval(self):
        configuration = self.config['systembeat.monitors']

        value = configuration.get('schedule')
        
        return ConfigurationItem(value)

    def shipToElasticsearch(self):
        configuration = self.config['output.elasticsearch']

        if configuration and configuration.get('hosts'):
            return True
        
        return False


    def getElasticHosts(self):
        configuration = self.config['output.elasticsearch']

        hosts = configuration.get('hosts')

        returnValue = []

        for host in hosts:
            returnValue.append(ConfigurationItem(host.split(':')[0]))

        return returnValue


    def getElasticPorts(self):
        configuration = self.config['output.elasticsearch']

        hosts = configuration.get('hosts')

        returnValue = []

        for host in hosts:
            returnValue.append(ConfigurationItem(host.split(':')[1]))

        return returnValue


    def getLogPath(self):
        configuration = self.config['paths']

        value = configuration.get('log')
        
        return ConfigurationItem(value)


    def getLogSize(self):
        configuration = self.config['paths']

        value = configuration.get('maxsize')
        
        return ConfigurationItem(value)