import json
import os

import requests

from actions.utils import ROOT_DIR, repo, owner


class ClientException(Exception):
    pass


class MissingTokenException(ClientException):
    pass


class Client:
    token = None

    def __init__(self, token=os.environ.get('GITHUB_TOKEN')):
        self.token = token

    @property
    def headers(self):
        return {'Authorization': f'token {self.token}'}

    def request(self, query_file, variables):
        if self.token is None:
            raise MissingTokenException("Tried to make a request with no authorization token")
        with open(os.path.join(ROOT_DIR, 'graphql', query_file)) as f:
            query = f.read()
        repo_slash_owner = os.environ['GITHUB_REPOSITORY']
        body = {
            'query': query,
            'variables': {
                **variables,
                'repo': repo(repo_slash_owner),
                'owner': owner(repo_slash_owner)
            }
        }
        return json.loads(requests.post(url='https://api.github.com/graphql', headers=self.headers, json=body).content)
