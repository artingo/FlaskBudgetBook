from bson import ObjectId

from backend.crud_repository import CrudRepository
from model.category import Category
from model.transaction import Transaction, TransactionType


class DbTransactions(CrudRepository):
    def __init__(self, mongo):
        super().__init__(mongo.db.transactions)
        print("Connected to 'transactions' collection")

    def read(self, _id: str) -> Transaction | None:
        result = super().read(_id)
        if result:
            return Transaction(
                result["user_id"],
                result["kind"],
                result["description"],
                result["category_id"],
                result["amount"],
                result["date"]
            )

        print(f"Could not find category with id: {_id}")
        return None