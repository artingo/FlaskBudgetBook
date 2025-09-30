from bson import ObjectId


class DbUsers:
    """
    This file provides CRUD operations for the "users" collection

    Attributes
    ----------
    collection - the user collection in the DB

    Methods
    -------
    create(firstname, surname)
    read(id)
    update(id, firstname, surname)
    delete(id)
    """

    def __init__(self, mongo):
        self.collection = mongo.db.users
        print("Connected to 'users' collection")

    def create(self, firstname: str, surname: str) -> str:
        """
        Creates a new user
        :param firstname: the first name
        :param surname: the surname
        :return: the newly created user_id
        """
        result = self.collection.insert_one({
            "firstname": firstname,
            "surname": surname
        })
        return str(result.inserted_id)

    def read(self, user_id: str):
        """
        Reads a user based on its user_id
        :param user_id: the ID of the user you are looking for
        :return: the user found or 'None' if none was found
        """
        user = self.collection.find_one({"_id": ObjectId(user_id)})

        if user:
            return user

        print(f"User with id {user_id} not found!")
        return None

    def read_all(self) -> list:
        """
        Reads all users from the collection
        :return: userList
        """
        return self.collection.find()

    def update(self, user_id: str, firstname: str, surname: str) -> bool:
        """
        Updates a user based on its user_id
        :param user_id: the ID of the user to be updated
        :param firstname: the new first name
        :param surname: the new surname
        :return: True if the update was successful - False if not
        """
        result = self.collection.update_one(
            { "_id": ObjectId(user_id)},
            {
                "$set": {
                    "firstname": firstname,
                    "surname": surname
                }
            })
        return result.acknowledged

    def delete(self, user_id: str) -> bool:
        """
        Deletes a user based on its user_id
        :param user_id: die ID des zu löschenden Benutzers
        :return: True, wenn das Löschen geklappt hat - False, falls nicht
        """
        result = self.collection.delete_one({"_id": ObjectId(user_id)})
        return result.deleted_count > 0

