from unittest import TestCase
from flask import Flask
from backend.db import init_db
from backend.users import DbUsers

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
        user_id = self.db.create('Annette', 'Ganz')
        assert user_id is not None
        print(f"User with ID {str(user_id)} created")

        # remember the user_id for cleanup at tear down.
        self.id_list.append(str(user_id))

    def test_create_duplicate(self):
        user_id = self.db.create('annette', 'ganz')
        assert user_id is None
        print(f"User already exists!")

    def test_read(self):
        if self.id_list:
            user_id = self.id_list[0]
            user = self.db.read(user_id)
            assert user is not None
            print("User read: ", user)

    def test_read_negative(self):
        user_id = '123456789012'
        user = self.db.read(user_id)
        assert user is None
        print(f"User with id {user_id} does not exist")

    def test_update(self):
        if self.id_list:
            user_id = self.id_list[0]
            success = self.db.update(user_id, "Brigitte", "Ganz")
            assert success is True
            print(f"First name changed to 'Brigitte'")

    def test_delete(self):
        if self.id_list:
            user_id = self.id_list[0]
            success = self.db.delete(user_id)
            assert success is True
            print(f"User with ID {user_id} deleted")
