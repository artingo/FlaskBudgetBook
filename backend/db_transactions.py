from bson import ObjectId
from backend.crud_repository import CrudRepository
from model.transaction import TransactionType

class DbTransactions(CrudRepository):
    # pipeline to collect transactions with users and categories
    PIPELINE = [
            {"$lookup": {
                "from": "users",
                "localField": "user_id",
                "foreignField": "_id",
                "as": "user"
            }},
            {"$unwind": "$user"},
            {"$lookup": {
                "from": "categories",
                "localField": "category_id",
                "foreignField": "_id",
                "as": "category"
            }},
            {"$unwind": "$category"},
            {"$project": {
                "username": {
                    "$concat": ["$user.firstname", " ", "$user.lastname"]
                },
                "type": "$kind",
                "description": "$description",
                "category_name": "$category.description",
                "amount": "$amount",
                "modified": {
                    "$dateToString": {
                        "date": "$date",
                        "format": "%d/%m/%Y %H:%M:%S"
                    }
                },
            }}
        ]

    def __init__(self, db):
        super().__init__(db.transactions)
        print("Connected to 'transactions' collection")

    def read_one(self, _id: str):
        """
        Read one transaction with user and category
        :param _id: the id of the transaction
        :return: a transaction as dictionary
        """
        single_pipeline = [{"$match": {"_id": ObjectId(_id)}}] + self.PIPELINE
        result = next(self.collection.aggregate(single_pipeline))
        # transform TransactionType value to name
        result['type'] = TransactionType(result['type']).name
        return result

    def read_all(self, **kwargs):
        """
        Reads all transactions with user and category
        :param kwargs: optional arguments
        :return: a list of transactions as dictionary
        """
        results = list(self.collection.aggregate(self.PIPELINE))
        # convert TransactionType values to names
        for r in results:
            r['type'] = TransactionType(r['type']).name
        return results
