from typing import Union, Dict, List, Any
from requests.auth import HTTPBasicAuth
from rest import RestClient


GITHUB_DEFAULT_HEADERS = {'Accept': 'application/vnd.github.v3+json',
                          'User-Agent': 'python-requests'}

JSONType = Union[None, bool, int, float, str, List[Any], Dict[str, Any]]


class GitHubError(Exception):
    """
    Error from GitHub REST API.
    """


class GitHubClient(RestClient):
    BASE_URL = 'https://api.github.com'

    def __init__(self, username: str, token: str, headers: Dict[str, str] = None):
        auth = HTTPBasicAuth(username, token)
        headers = headers or GITHUB_DEFAULT_HEADERS

        super().__init__(self.BASE_URL, auth=auth, headers=headers)

    def __enter__(self):
        return self

    @property
    def username(self) -> str:
        return self._session.auth.username

    @username.setter
    def username(self, username: str):
        self._session.auth.username = username

    @property
    def token(self) -> str:
        return self._session.auth.password

    @token.setter
    def token(self, token: str):
        self._session.auth.password = token

    def get_public_repos(self) -> List[Dict[str, Any]]:
        return self.get('user/repos', params={'visibility': 'public'})

    def get_user(self, user: str) -> Dict[str, Any]:
        return self.get(f'users/{user}')
