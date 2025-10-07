from backend.crud_repository import CrudRepository
from model.transaction import Transaction, TransactionType


class DbTransactions(CrudRepository):
    def __init__(self, db):
        super().__init__(db.transactions)
        print("Connected to 'transactions' collection")

    #TODO: query with users and categories