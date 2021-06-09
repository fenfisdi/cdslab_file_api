from dataclasses import dataclass

from requests import Request, Session
from requests.models import Response


@dataclass
class API:
    url: str


class APIService:
    """
    Class for http request management
    """
    def __init__(self, api: API):
        """
        Class constructor
        """
        self.api = api
        self.session = Session()

    def __url(self, endpoint: str) -> str:
        return "".join([self.api.url, endpoint])

    def post(
            self,
            endpoint: str,
            data: dict = None,
            parameters: dict = None
    ) -> Response:
        """
        Make a POST request
        :param endpoint: API endpoint
        :param data: data for consultation
        :param parameters: parameters for consultation
        """
        request = Request(
            url=self.__url(endpoint),
            method='POST',
            params=parameters,
            json=data

        ).prepare()
        return self.session.send(request)

    def get(self, endpoint: str, parameters: dict = None) -> Response:
        """
        Make a GET request
        :param endpoint: API endpoint
        :param parameters: parameters for consultation
        """
        request = Request(
            url=self.__url(endpoint),
            method='GET',
            params=parameters
        ).prepare()
        return self.session.send(request)
