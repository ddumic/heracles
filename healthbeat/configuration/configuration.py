import yaml

class ConfigurationItem(object):
    value = ''

    def __init__(self, value):
        self.value = value


class Configuration(object):
    
    config = yaml.load(open('healthbeat.yml'))


    def getUrls(self):
        configuration = self.config['healthbeat.monitors']
        
        values = configuration.get('urls')

        returnValue = []

        for value in values:
            returnValue.append(ConfigurationItem(value))

        return returnValue


    def getInterval(self):
        configuration = self.config['healthbeat.monitors']

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

