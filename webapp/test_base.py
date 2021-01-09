from flask_testing import TestCase  # type: ignore
from . import create_app


class BaseTestCase(TestCase):

    def create_app(self):
        app = create_app()
        return app
