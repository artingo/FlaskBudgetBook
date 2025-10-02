from unittest import TestCase
from bson import ObjectId
from flask import Flask
from backend.db import init_db
from backend.categories import DbCategories

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
        description = "Monthly income"
        new_category = self.db.create(description)
        assert new_category is not None

        # remember the _id for cleanup at tear down.
        if new_category:
            self.id_list.append(new_category.id)


    def test_create_duplicate(self):
        duplicate_category = self.db.create("Monthly income")
        # remember the _id for cleanup at tear down.
        if duplicate_category:
            self.id_list.append(duplicate_category.id)

        duplicate_category = self.db.create("Monthly income")
        assert duplicate_category is None

    # FixMe: reapair test
    def test_read(self):
        if not self.id_list:
            self.test_create()
        _id = self.id_list[0]
        print(f"_id = {_id}")
        category = self.db.read(_id)
        assert category is not None

    def test_read_negative(self):
        non_existing_id = ObjectId()
        category = self.db.read(non_existing_id)
        assert category is None

    def test_update(self):
        if self.id_list:
            _id = self.id_list[0]
            success = self.db.update(_id, "")
            assert success is True

    def test_delete(self):
        if self.id_list:
            _id = self.id_list[0]
            success = self.db.delete(_id)
            assert success is True
        else:
            self.fail()
