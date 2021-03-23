import mock
from uuid import uuid4
from .test_base import BaseTestCase
from .models import User, Task, Status


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


class TaskModelTest(BaseTestCase):

    def test_task_model(self):
        user = User(name='name')
        task = Task(name='test', user=user, uuid=uuid4())
        assert task.user == user
        assert task in user.tasks
        assert str(task.uuid) in task.url
        assert task.status == Status.processing

    def test_task_name_error_when_longer_than_64_chars(self):
        Task(name="x" * 64)
        with self.assertRaises(AssertionError):
            Task(name="x" * 128)
