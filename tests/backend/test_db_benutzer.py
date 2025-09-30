from unittest import TestCase
from flask import Flask
from backend.db import init_db
from backend.users import DbUsers


class Test(TestCase):
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

    @classmethod
    def tearDownClass(cls):
        """
        This method is run after all tests. It closes the MongoDB connection.
        """
        cls.mongo.cx.close()

    def test_create(self):
        user_id = self.db.create('Annette', 'Ganz')
        assert user_id is not None
        self._id = user_id
        print(f"User with ID {str(user_id)} created")

    def test_read(self):
        if not hasattr(self, "_id"):
            self.test_create()
        user = self.db.read(self._id)
        assert user is not None
        print(f"User with ID {str(self._id)} read")
        print("User: ", user)

    def test_update(self):
        if not hasattr(self, "_id"):
            self.test_read()
        self.db.delete(self._id)
        print(f"User with ID {str(self._id)} deleted")

    def test_delete(self):
        self.test_read()
        self.db.update(self._id, "Brigitte", "Ganz")
        print(f"First name changed to 'Brigitte'")
