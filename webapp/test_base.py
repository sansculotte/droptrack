from flask_testing import TestCase  # type: ignore
from . import create_app
#from .models import db


class BaseTestCase(TestCase):

    def create_app(self):
        app = create_app()
        return app

#    def setUp(self):
#        super().setUp()
#        assert db.engine.url.database.endswith('_testing')
#        db.create_all()
#
#    def tearDown(self):
#        super().tearDown()
#        assert db.engine.url.database.endswith('_testing')
#        db.session.close()
#        db.drop_all()
