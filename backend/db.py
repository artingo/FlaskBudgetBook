from flask_pymongo import PyMongo
from flask import Flask
mongo = PyMongo()

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