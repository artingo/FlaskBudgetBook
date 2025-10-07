from backend.crud_repository import CrudRepository
from model.transaction import Transaction, TransactionType


class DbTransactions(CrudRepository):
    def __init__(self, mongo):
        super().__init__(mongo.db.transactions)
        print("Connected to 'transactions' collection")

    #TODO: query with users and categories