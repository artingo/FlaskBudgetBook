import random
import string
from unittest import TestCase
from flask import Flask
from backend.db import init_db
from backend.db_categories import DbCategories
from model.category import Category


class TestCategories(TestCase):
    """
    Test cases for the DbCategories class.
    """

    @classmethod
    def setUpClass(cls):
        """
        This method is run before all tests. It creates a MongoDB connection.
        """
        app = Flask(__name__)
        cls.mongo = init_db(app)
        cls.db = DbCategories(cls.mongo)
        cls.id_list = []

    @classmethod
    def tearDownClass(cls):
        """
        This method is run after all tests.
        It deletes all created categories and closes the MongoDB connection.
        """
        # delete all created categories
        for _id in cls.id_list:
            cls.db.delete(_id)
        # close the connection
        cls.mongo.cx.close()

    def test_create(self):
        new_id = self.create_dummy_category()
        assert new_id is not None

    def test_create_duplicate(self):
        # 1. create a test category
        cat_id = self.db.create("Test Category")
        self.id_list.append(cat_id)
        #2 create same category with lower case
        duplicate_id = self.db.create("test category")
        assert duplicate_id is None

    def test_read(self):
        _id = self.create_dummy_category()
        category = self.db.read(_id)
        assert category is not None

    def test_read_negative(self):
        with self.assertRaises(TypeError):
            self.db.read("xxx")

    def test_update(self):
        # 1. create a dummy category
        _id = self.create_dummy_category()
        updated_category = Category("Update Category")
        # 2. update existing category
        success = self.db.update(_id, updated_category)

    def test_delete(self):
        # 1. create a dummy category
        _id = self.create_dummy_category()
        # 2. delete dummy category
        success = self.db.delete(_id)
        assert success is True

    def create_dummy_category(self):
        category = ''.join(random.choices(string.ascii_letters, k=10))
        _id = self.db.create(category)
        # remember the user_id for cleanup at tear down.
        self.id_list.append(_id)
        return _id