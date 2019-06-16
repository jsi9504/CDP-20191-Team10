import requests


class Orchestrator:
    token = None
    startJobs = ''
    Jobs = ''

    def __init__(self, tenant, user, password, url='https://platform.uipath.com/'):
        self.url = url
        self.token = self.__getToken(tenant, user, password)
        self.startJobs = 'odata/Jobs/UiPath.Server.Configuration.OData.StartJobs'
        self.Jobs = 'odata/Jobs'


    def __getToken(self, tenant, user, password):
        res = self.request('POST', 'api/account/authenticate',
                           {'tenancyName': tenant,
                            'usernameOrEmailAddress': user,
                            'password': password})
        print(res)
        return res["result"]


    def request(self, type, extension, body=None):
        uri = self.url + extension
        headers = self.__getHeaders(extension)

        response = requests.request(type.upper(), uri, data=body, headers=headers)

        return response.json()

    def __getHeaders(self, extension):
        if extension == self.startJobs:
            headers = {'Authorization': 'Bearer ' + str(self.token),
                       'Content-type': 'application/json'}
        else:
            headers = {'Authorization': 'Bearer ' + str(self.token) or ''}

        return headers
