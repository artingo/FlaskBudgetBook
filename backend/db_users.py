import re
from backend.crud_repository import CrudRepository
from model.user import User

class DbUsers(CrudRepository):
    """
    This file provides CRUD operations for the "users" collection

    Attributes
    ----------
    collection - the new_user collection in the DB

    Methods
    -------
    create(firstname, lastname)
    read(_id)
    update(_id, firstname, lastname)
    delete(_id)
    """

    def __init__(self, mongo):
        # pass the collection to the base class
        super().__init__(mongo.db.users)
        print("Connected to 'users' collection")

    def create(self, new_user: User) -> str | None:
        """
        Creates a new user
        :param new_user: the user to create
        :return: the newly created user_id
        :rtype: str | None
        """
        # if an new_user with the same name exists...
        firstname_lower = re.compile(new_user.firstname, re.IGNORECASE)
        lastname_lower = re.compile(new_user.lastname, re.IGNORECASE)
        existing_user = self.collection.find_one({"firstname": firstname_lower, "lastname": lastname_lower})

        # ... then don't create this new_user
        if existing_user:
            return None

        new_id = super().create(new_user)
        return new_id