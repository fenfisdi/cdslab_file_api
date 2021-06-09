from typing import Optional, Union

from fastapi.responses import UJSONResponse as FastAPIResponse
from requests.models import Response


class UJSONResponse(FastAPIResponse):
    """
        Create the standard response for the endpoints 
    """
    def __init__(
        self,
        message: str,
        status_code: int,
        data: Optional[Union[dict, list]] = None
    ):
        """
        Constructor of class
        
        :param message: Response of process.
        :param status_code: HTTP code.
        :param data: Data of process.
        """
        response = dict(
            message=message,
            status_code=status_code,
            data=data,
        )
        super().__init__(response, status_code)


def to_response(response: Response) -> UJSONResponse:
    data = response.text
    message = 'API Error'
    if response.headers.get('content-type') == 'application/json':
        data = response.json()
        message = data.get('message', message)
        data = data.get('data', data)
    return UJSONResponse(message, response.status_code, data)
