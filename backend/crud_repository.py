from typing import Dict, Any, List
from bson import ObjectId
from flask_pymongo.wrappers import Collection

class CrudRepository:
    """
    A generic CRUD repository.
    """
    def __init__(self, collection: Collection):
        """
        Initialize the repository with the corresponding collection.
        :param collection: the collection to use.
        """
        self.collection = collection

    def create(self, document: object) -> str:
        """
        Create a new document in the collection.
        :param document: a dictionary with the proper key-value pairs.
        :return: the ObjectId of the newly created document.
        """
        dictionary = vars(document)
        result = self.collection.insert_one(dictionary)
        return str(result.inserted_id)

    def read(self, _id: str) -> Dict[str, Any]:
        """
        Retrieve a document from the collection.
        :param _id: the ObjectId of the document.
        :return: a dictionary with key-value pairs, corresponding to the document type.
        """
        object_id = self.to_object_id(_id)
        return self.collection.find_one({"_id": object_id})

    def read_all(self, query: Dict[str, Any] = {}) -> List[Dict[str, Any]]:
        """
        Retrieve all documents from the collection.
        :param query: an optional query dictionary.
        :return: the list of documents.
        """
        return list(self.collection.find(query))

    def update(self, _id: str, document: object) -> bool:
        """
        Update a document in the collection.
        :param _id: the ObjectId of the document.
        :param document: a dictionary with the proper key-value pairs.
        :return: True if successful, False otherwise.
        """
        object_id: ObjectId = self.to_object_id(_id)
        dictionary = vars(document)
        result = self.collection.update_one(
            {"_id": object_id},
            {"$set": dictionary})
        return result.modified_count == 1

    def delete(self, _id: str) -> bool:
        """
        Delete a document from the collection.
        :param _id: the ObjectId of the document.
        :return: True if successful, False otherwise.
        """
        object_id = self.to_object_id(_id)
        result = self.collection.delete_one({"_id": object_id})
        return result.deleted_count == 1

    @staticmethod
    def to_object_id(_id: str) -> ObjectId:
        """
        Converts a String into a ObjectId.
        Raises a TypeError if the '_id' is not an ObjectId.
        :param _id: the ObjectId as String.
        :return: the resulting ObjectId
        """
        if ObjectId.is_valid(_id):
            return ObjectId(_id)
        raise TypeError("Invalid ObjectId: '%s'" % _id)