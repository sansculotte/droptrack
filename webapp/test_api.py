from typing import Callable
import mock
from contextlib import contextmanager
from .test_base import BaseTestCase
from .models import User


class ApiTests(BaseTestCase):

    @contextmanager
    def api_key(self, key='xxx'):
        with mock.patch('webapp.models.User.find_by_api_key') as m:
            m.return_value = User(name='test')
            yield m

    def request(self, method: Callable, path: str, data=None):
        key = 'xxx'
        with self.api_key(key):
            result = method(path, headers={'x-authentication': key})
            return result

    def get(self, path):
        return self.request(self.client.get, path)

    def delete(self, path):
        return self.request(self.client.delete, path)

    # tests
    def test_file_list_forbidden(self):
        result = self.client.get('/files')
        self.assert403(result)
        assert result.json['data']['message'] == 'Missing API key'

    def test_file_list_not_found(self):
        result = self.get('/files')
        self.assert404(result)

    def test_file_not_found(self):
        result = self.get('/files/xxx')
        self.assert404(result)

    def test_file_delete_not_found(self):
        result = self.delete('/files/xxx')
        self.assert404(result)

    def test_not_found_is_json(self):
        result = self.get('/uzwterwqr')
        self.assert404(result)
        assert result.json['data']['message'] == (
            'The requested URL was not found on the server.'
            ' '
            'If you entered the URL manually please check your spelling and'
            ' '
            'try again.'
        )
