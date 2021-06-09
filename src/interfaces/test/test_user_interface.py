from unittest import TestCase

from mongoengine import connect, disconnect

from src.interfaces.user import UserInterface
from src.models.db.user import User


class UserInterfaceTestCase(TestCase):

    def setUp(self):
        connect('mongoenginetest', host='mongomock://localhost')

        self.email = 'test2@test.com'
        User(
            name='testName',
            email=self.email
        ).save()

    def tearDown(self):
        disconnect()

    def test_find_one_successful(self):
        user = UserInterface.find_one(self.email)

        self.assertIsNotNone(user)
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, self.email)

    def test_find_one_not_found(self):
        user = UserInterface.find_one('test1@test.com')

        self.assertIsNone(user)
