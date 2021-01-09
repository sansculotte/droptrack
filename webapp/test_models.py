import mock
from .test_base import BaseTestCase
from .models import User


class UserModelTest(BaseTestCase):

    def test_user_model_instanciation(self):
        user = User(name='name', api_key='api_key_XXX')
        assert user.name == 'name'
        assert user.api_key == 'api_key_XXX'

    @mock.patch('webapp.models.User.make_home_directory')
    def test_user_create(self, m):
        name = 'name'
        email = 'email@0.com'
        password = '1134'
        user = User.create(name=name, email=email, password=password)
        assert user.name == name
        assert user.email == email
        assert user.check_password(password)
        assert m.call_count == 1
