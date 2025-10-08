from bson import ObjectId
from backend.crud_repository import CrudRepository
from model.transaction import TransactionType


class DbTransactions(CrudRepository):
    def __init__(self, db):
        super().__init__(db.transactions)
        print("Connected to 'transactions' collection")

    def read_one(self, _id: str):
        pipeline = [
            {"$match": {"_id": ObjectId(_id)}},
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
                        "format": "%m/%d/%Y %H:%M:%S"
                    }
                },
            }}
        ]
        result = next(self.collection.aggregate(pipeline))
        # transform TransactionType value to name
        result['type'] = TransactionType(result['type']).name
        return result

    # TODO: read all transactions with username and category_description