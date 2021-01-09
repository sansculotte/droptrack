from .test_base import BaseTestCase


class ApiTests(BaseTestCase):

    def test_file_list(self):
        result = self.client.get('/files')
        self.assert403(result)
