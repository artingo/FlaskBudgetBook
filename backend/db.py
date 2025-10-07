import pymongo
from flask import Flask
from flask_pymongo import PyMongo
from backend.db_categories import DbCategories
from backend.db_transactions import DbTransactions
from backend.db_users import DbUsers

mongo = PyMongo()
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client.get_database('budgetbook')

# initialize backend
dbUsers = DbUsers(db)
dbCategories = DbCategories(db)
dbTransactions = DbTransactions(db)

"""
Creates the MongoDB connection
"""
def init_db(app: Flask):
    """
    Initializes the DB connection
    :param app: the Flask app
    :return: the DB connection
    """
    app.config["MONGO_URI"] = "mongodb://localhost:27017/budgetbook"
    mongo.init_app(app)
    return mongo