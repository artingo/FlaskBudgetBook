from flask import Flask
from backend.db import mongo, init_db
"""
This script handles DB connection and URL routes 
"""
app = Flask(__name__)
init_db(app)
@app.route('/')
def root():
    """
    Reacts to the root URL, i.e. "/".
    Currently, shows the succesfuls DB connection.
    """
    return f"DB connection: {mongo.db}"

if __name__ == '__main__':
    app.run()