from bson import ObjectId


class Category:
    def __init__(self, description: str, _id: ObjectId=None):
        self.description = description
        self.id = _id
