from bson import ObjectId
from model.category import Category

class DbCategories:
    """
    The class that handles transaction categories in the database.
    """
    def __init__(self, mongo):
        self.collection = mongo.db.categories
        print("Connected to 'categories' collection")

    def create(self, description: str) -> Category | None:
        """
        Creates a new category. Checks for duplicates.
        :param description: the description of the new category
        :return: Category if successful, 'None' if failed
        """
        # check for existing category
        existing_category = self.collection.find_one({"description": description})
        if existing_category:
            return None

        result = self.collection.insert_one({"description": description})
        new_category = Category(description, result.inserted_id)
        return new_category

    def read(self, _id: ObjectId) -> Category | None:
        """
        Retrieves a category by id.
        :param _id: the ObjectId of the category to retrieve
        :return: Category if successful, 'None' if failed
        """
        category = self.collection.find_one({"_id": _id})
        if category:
            return category

        # if category doesn't exist, return 'None'
        print(f"Category with ID '{_id}' not found")
        return None

    def update(self, _id: ObjectId, description: str) -> bool:
        """
        Updates a category by id.
        :param _id: the ObjectId of the category to be updated
        :param description: the new description
        :return: 'True' if successful, 'False' if failed
        """
        result = self.collection.update_one(
            {"_id": _id},
            {
                "$set": {"description": description}
            })
        return result.acknowledged

    def delete(self, _id: ObjectId) -> bool:
        """
        Deletes a category by id.
        :param _id: the ObjectId of the category to be deleted
        :return: 'True' if successful, 'False' if failed
        """
        result = self.collection.delete_one({"_id": _id})
        return result.deleted_count > 0
