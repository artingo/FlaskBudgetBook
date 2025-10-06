import random
import string
from unittest import TestCase
from flask import Flask
from backend.db import init_db
from backend.db_users import DbUsers
from model.user import User


class TestUsers(TestCase):
    """
    This test class tests the CRUD operations for the "users" collection
    """
    @classmethod
    def setUpClass(cls):
        """
        This method is run before all tests. It creates a MongoDB connection.
        """
        app = Flask(__name__)
        cls.mongo = init_db(app)
        cls.db = DbUsers(cls.mongo)
        cls.id_list = []

    @classmethod
    def tearDownClass(cls):
        """
        This method is run after all tests. It closes the MongoDB connection.
        """
        # delete all created users
        for user_id in cls.id_list:
            cls.db.delete(user_id)
        # close the connection
        cls.mongo.cx.close()

    def test_create(self):
        user_id = self.create_dummy_user()
        assert user_id is not None

    def test_create_duplicate(self):
        # 1. create a new_user
        user_id = self.db.create(User('Annette', 'Ganz'))
        self.id_list.append(user_id)
        # 2. create a new_user with same, lower case name
        user_id = self.db.create(User('annette', 'ganz'))
        assert user_id is None

    def test_read(self):
        # 1. create a dummy new_user
        users_id = self.create_dummy_user()
        # 2. read dummy new_user
        user = self.db.read(users_id)
        assert user is not None

    def test_read_negative(self):
        user_id = '123456789012'
        with self.assertRaises(TypeError):
            self.db.read(user_id)

    def test_update(self):
        # 1. create a dummy new_user
        _id = self.create_dummy_user()
        update_user = User("Tommy", "Cash")
        # 2. update existing new_user
        success = self.db.update(_id, update_user)
        assert success is True

    def test_delete(self):
        # 1. create a dummy new_user
        user_id = self.create_dummy_user()
        success = self.db.delete(user_id)
        assert success is True

    def create_dummy_user(self):
        """
        This method creates a dummy new_user
        :return: the id of the freshly created
        """
        firstname = ''.join(random.choices(string.ascii_letters, k=8))
        user = User(firstname, 'Test-User')
        _id = self.db.create(user)
        # remember the user_id for cleanup at tear down.
        self.id_list.append(_id)
        return _id
