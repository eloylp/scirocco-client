import json

from urllib3.request import urlencode


class RequestsAdapter:
    from_header = "Scirocco-From"

    def __init__(self, api_url, node_id, auth_token, request_manager, request_manager_response_handler):
        self._api_url = api_url
        self._node_id = node_id
        self._auth_token = auth_token
        self.request_manager = request_manager
        self.request_manager_response_handler = request_manager_response_handler

    @property
    def api_url(self):
        return self._api_url

    @property
    def node_id(self):
        return self._node_id

    @property
    def auth_token(self):
        return self._auth_token

    def get_fixed_headers(self):

        return {
            self.from_header: self._node_id,
            'Authorization': self._auth_token
        }

    def get_uri(self, resource):

        url = '/'.join([self.api_url, resource.strip("/")])
        return url

    def request(self, method, resource='', data=None, headers=None):

        method = method.upper()
        url = self.get_uri(resource)

        if isinstance(headers, dict):
            headers.update(self.get_fixed_headers())
        else:
            headers = self.get_fixed_headers()

        if isinstance(data, dict):

            if method in ['GET', 'DELETE']:
                url = ''.join([url, '?', urlencode(data)])
                data = None
            else:
                data = json.dumps(data)
        request_manager_result = self.request_manager.urlopen(method, url, headers=headers, body=data)

        return self.request_manager_response_handler.handle(request_manager_result)


class RequestManagerResponseHandler:
    def handle(self, response):
        ro = RequestAdapterResponse()

        ro.http_headers = self.treat_headers(response.headers)
        ro.http_status = response.status
        ro.system_data = self.extract_system_data(response.headers)
        ro.message_data = self.treat_data(response.data)
        return ro

    def extract_system_data(self, headers):

        return {k: v for k, v in headers.items() if k in self.get_system_headers()}

    def treat_data(self, data):

        try:

            if isinstance(data, bytes):
                try:
                    return json.loads(data.decode())
                except ValueError:
                    return data.decode()
            if isinstance(data, str):
                return json.loads(data)
            if isinstance(data, (object, dict)):
                return data
            return data
        except ValueError or TypeError:
            return data

    def treat_headers(self, headers):

        return headers

    @staticmethod
    def get_system_headers():
        return [

            "Scirocco-From",
            "Scirocco-To",
            "Scirocco-Id",
            "Scirocco-Topic",
            "Scirocco-Status",
            "Scirocco-Update-Time",
            "Scirocco-Created-Time",
            "Scirocco-Scheduled-Time",
            "Scirocco-Error-Time",
            "Scirocco-Processed-Time",
            "Scirocco-Tries"
        ]


class RequestAdapterResponse:
    def __init__(self):
        self._system_data = None
        self._message_data = None
        self._http_headers = None
        self._http_status = None

    ## TODO this atributte can be another object (composition) beause this fields are well defined at server side model.
    @property
    def system_data(self):
        return self._system_data

    @system_data.setter
    def system_data(self, data):
        self._system_data = data

    @property
    def message_data(self):
        return self._message_data

    @message_data.setter
    def message_data(self, data):
        self._message_data = data

    @property
    def http_headers(self):
        return self._http_headers

    @http_headers.setter
    def http_headers(self, data):
        self._http_headers = data

    @property
    def http_status(self):
        return self._http_status

    @http_status.setter
    def http_status(self, status):
        self._http_status = status
