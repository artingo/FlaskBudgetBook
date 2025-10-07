import re
from typing import List, Dict, Any
from backend.crud_repository import CrudRepository
from model.category import Category

class DbCategories(CrudRepository):
    """
    The class that handles transaction categories in the database.
    """

    def __init__(self, db):
        # pass the collection to the base class
        super().__init__(db.categories)
        print("Connected to 'categories' collection")

    def create(self, description: str) -> str | None:
        """
        Creates a new category. Checks for duplicates.
        :param description: the description of the new category
        :return: the ID of the new category if successful, 'None' otherwise.
        """
        # check for existing category
        description_lower = re.compile(description, re.IGNORECASE)
        existing_category = self.collection.find_one({
            "description": description_lower
        })
        if existing_category:
            return None

        new_category = Category(description)
        return super().create(new_category)

    # def read(self, _id: str) -> Category | None:
    #     """
    #     Reads a category from the database.
    #     :param _id: the ObjectId of the document.
    #     :return: the category if successful, 'None' otherwise.
    #     """
    #     result = super().read(_id)
    #     if result:
    #         return Category(result["description"])
    #
    #     print(f"Could not find category with id: {_id}")
    #     return None

    def read_all(self) -> List[Dict[str, Any]]:
        return super().read_all('description')

