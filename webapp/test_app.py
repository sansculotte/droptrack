from .test_base import BaseTestCase


class AppTests(BaseTestCase):

    def test_ensure_json_response(self):
        result = self.client.get('/quzwrquwe')
        self.assert404(result)
        data = result.json['data']
        assert data['message'] == (
            'The requested URL was not found on the'
            ' '
            'server. If you entered the URL manually please check your'
            ' '
            'spelling and try again.'
        )
