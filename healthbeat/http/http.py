import httplib

class HttpResponse(object):
    endpoint = ''
    responseStatus = ''
    responseCode = ''

    def __init__(self, endpoint, responseStatus, responseCode):
        self.endpoint = endpoint
        self.responseStatus = responseStatus
        self.responseCode = responseCode

class HttpClient(object):

    def get(self, url):
        connection = httplib.HTTPSConnection(url)
        connection.request("GET", "/")
        response = connection.getresponse()

        return HttpResponse(url, response.reason, response.status)