import yaml
import win32con
import win32service

class ConfigurationItem(object):
    value = ''

    def __init__(self, value):
        self.value = value


class Configuration(object):
    
    config = yaml.load(open('servicebeat.yml'))

    def listServices(self):
        resume = 0
        accessSCM = win32con.GENERIC_READ
        accessSrv = win32service.SC_MANAGER_ALL_ACCESS

        #Open Service Control Manager
        hscm = win32service.OpenSCManager(None, None, accessSCM)

        #Enumerate Service Control Manager DB
        typeFilter = win32service.SERVICE_WIN32
        stateFilter = win32service.SERVICE_STATE_ALL

        statuses = win32service.EnumServicesStatus(hscm, typeFilter, stateFilter)

        return statuses

    def getServices(self):
        configuration = self.config['servicebeat.config.modules']
        
        services = configuration.get('services')

        returnValue = []

        if services[0] == '*':
            statuses = self.listServices()
            for (short_name, desc, status) in statuses:
                returnValue.append(ConfigurationItem(short_name))

        else:
            for service in services:
                returnValue.append(ConfigurationItem(service))

        return returnValue


    def getInterval(self):
        configuration = self.config['servicebeat.config.modules']

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
