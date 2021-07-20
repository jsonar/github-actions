import json
import os

import requests


class ClientException(Exception):
    pass


class MissingTokenException(ClientException):
    pass


class Client:
    token = None
    base_url = 'https://api.github.com/'

    def __init__(self, token=os.environ.get('GITHUB_TOKEN')):
        self.token = token

    @property
    def headers(self):
        return {
            'Accept': 'application/vnd.github.starfox-preview+json, application/vnd.github.inertia-preview+json,'
                      'application/vnd.github.v3+json',
            'Authorization': f'token {self.token}'
        }

    def request(self, method, url):
        if self.token is None:
            raise MissingTokenException("Tried to make a request with no authorization token")
        return json.loads(requests.request(method=method, url=self.base_url+url, headers=self.headers).content)
