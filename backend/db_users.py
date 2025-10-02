import re
from typing import Any

from bson import ObjectId


class DbUsers:
    """
    This file provides CRUD operations for the "users" collection

    Attributes
    ----------
    collection - the user collection in the DB

    Methods
    -------
    create(firstname, lastname)
    read(_id)
    update(_id, firstname, lastname)
    delete(_id)
    """

    def __init__(self, mongo):
        self.collection = mongo.db.users
        print("Connected to 'users' collection")

    def create(self, firstname: str, lastname: str) -> str | None:
        """
        Creates a new user
        :param firstname: the first name
        :param lastname: the last name
        :return: the newly created user_id
        """
        # if an user with the same name exists...
        firstname_lower = re.compile(firstname, re.IGNORECASE)
        lastname_lower = re.compile(lastname, re.IGNORECASE)
        existing_user = self.collection.find_one({"firstname": firstname_lower, "lastname": lastname_lower})

        # ... then don't create this user
        if existing_user:
            return None

        result = self.collection.insert_one({
            "firstname": firstname,
            "lastname": lastname
        })
        return str(result.inserted_id)

    def read(self, user_id: str) -> Any | None:
        """
        Reads a user based on its user_id
        :param user_id: the ID of the user you are looking for
        :return: the user found or 'None' if none was found
        """
        # check if user_id is valid
        if not ObjectId.is_valid(user_id):
            return None

        user = self.collection.find_one({"_id": ObjectId(user_id)})
        if user:
            return user

        print(f"User with _id {user_id} not found!")
        return None

    def read_all(self) -> list:
        """
        Reads all users from the collection
        :return: userList
        """
        return self.collection.find()

    def update(self, user_id: str, firstname: str, lastname: str) -> bool:
        """
        Updates a user based on its user_id
        :param user_id: the ID of the user to be updated
        :param firstname: the new first name
        :param lastname: the new lastname
        :return: True if the update was successful - False if not
        """
        # check if user_id is valid
        if not ObjectId.is_valid(user_id):
            return False

        result = self.collection.update_one(
            { "_id": ObjectId(user_id)},
            {
                "$set": {
                    "firstname": firstname,
                    "lastname": lastname
                }
            })
        return result.acknowledged

    def delete(self, user_id: str) -> bool:
        """
        Deletes a user based on its user_id
        :param user_id: die ID des zu löschenden Benutzers
        :return: True, wenn das Löschen geklappt hat - False, falls nicht
        """
        # check if user_id is valid
        # if not ObjectId.is_valid(user_id):
        #     return False

        result = self.collection.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count > 0

