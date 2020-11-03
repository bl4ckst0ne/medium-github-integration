from functools import partialmethod
from typing import Union, Dict, List, Any
import requests


JSONType = Union[None, bool, int, float, str, List[Any], Dict[str, Any]]


class RestError(Exception):
    """
    Error from REST API Client.
    """


class RestClient:
    def __init__(self, base_url: str, **session_kwargs):
        self.base_url = base_url
        self._session = requests.Session()

        for key, value in session_kwargs.items():
            setattr(self._session, key, value)

    def __enter__(self):
        return self

    def __exit__(self, *_):
        self.close()

    def close(self):
        return self._session.close()

    def request(self, method: str, path: str, **kwargs) -> JSONType:
        try:
            resp = self._session.request(method, f'{self.base_url}/{path}', **kwargs)
            resp.raise_for_status()
            return resp.json()
        except requests.HTTPError as http_error:
            raise RestError(f'Invalid request from {self.base_url}: {http_error}') from http_error
        except requests.RequestException as err:
            raise RestError(err) from err

    get = partialmethod(request, 'GET')
    post = partialmethod(request, 'POST')
    put = partialmethod(request, 'PUT')
    patch = partialmethod(request, 'PATCH')
    delete = partialmethod(request, 'DELETE')
    head = partialmethod(request, 'HEAD')
    options = partialmethod(request, 'OPTIONS')
