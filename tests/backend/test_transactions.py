import pprint
import random
from datetime import datetime, timezone
from unittest import TestCase
from flask import Flask

from backend.db import init_db, dbTransactions, dbUsers, dbCategories
from model.transaction import Transaction, TransactionType


class TestDbTransactions(TestCase):
    @classmethod
    def setUpClass(cls):
        """
        This method is run before all tests.
        It creates a MongoDB connection.
        """
        app = Flask(__name__)
        cls.mongo = init_db(app)
        cls.db = dbTransactions
        cls.id_list = []

        # read existing users
        db_users = dbUsers
        cls.users = db_users.read_all()

        # read existing categories
        db_categories = dbCategories
        cls.categories = db_categories.read_all()

    @classmethod
    def tearDownClass(cls):
        """
        This method is run after all tests.
        It closes the MongoDB connection.
        """
        # delete all created users
        for _id in cls.id_list:
            cls.db.delete(_id)
        # close the connection
        cls.mongo.cx.close()

    def test_create(self):
        transaction_id = self.create_dummy_transaction()
        assert transaction_id is not None

    def test_read(self):
        trans_id = self.create_dummy_transaction()
        transaction = self.db.read(trans_id)
        assert transaction is not None

    def test_read_negative(self):
        trans_id = '123456789012'
        with self.assertRaises(TypeError):
            self.db.read(trans_id)

    def test_update(self):
        trans_id = self.create_dummy_transaction()
        transaction = self.db.read(trans_id)
        transaction['amount'] = 99.99
        transaction['description'] = "Description changed"
        success = self.db.update(trans_id, transaction)
        assert success is True

    def test_delete(self):
        trans_id = self.create_dummy_transaction()
        success = self.db.delete(trans_id)
        assert success is True

    def test_read_one(self):
        trans_id = self.create_dummy_transaction()
        result = self.db.read_one(trans_id)
        assert result is not None
        pprint.pprint(result)

    def create_dummy_transaction(self) -> str:
        """
        This creates a dummy transaction.
        :return: the _id of the freshly created transaction.
        """
        first_user = self.users[0]
        user_id = first_user.get('_id')

        first_category = self.categories[0]
        category_id = first_category.get('_id')

        amount = round(random.uniform(1.0, 99.0), 2)

        transaction = Transaction(
            user_id,
            TransactionType.Income.value,
            "Random transaction",
            category_id,
            amount,
            datetime.now(timezone.utc)
        )
        _id = self.db.create(transaction)
        # remember the user_id for cleanup at tear down.
        self.id_list.append(_id)
        return _id