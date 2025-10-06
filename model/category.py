from bson import ObjectId


class Category:
    def __init__(self, description: str):
        self.description = description