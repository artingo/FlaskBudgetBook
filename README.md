# Flask / Mongo tutorial

This project is meant to teach flask and MongoDB fundamentals by creating a **<u>budget book</u>**, step by step. <br/>
It uses the [Flask](https://flask.palletsprojects.com/en/stable/quickstart/) web framework, a [Bootstrap 5](https://getbootstrap.com) frontend and stores its data in [MongoDB](https://www.digitalocean.com/community/tutorials/how-to-use-mongodb-in-a-flask-application).  

Follow these steps to implement the budget book:
## 1. Create project
1. In your IDE, create a new Flask project:<br/>
![New Flask project](screenshots/new_project.png)

1. Create the following directory structure:<br/>
   ![directory structure](screenshots/directories.png)

## 2. Database connection
1. [Download](https://www.mongodb.com/try/download/community) and install MongoDB.

1. Start MongoDB.  

1. Create a database connection script in [backend/db.py](backend/db.py):  
   ```python
   from flask_pymongo import PyMongo
   from flask import Flask
    
   mongo = PyMongo()
    
   def init_db(app: Flask):
     app.config["MONGO_URI"] = mongodb://localhost:27017/budgetbook"
     mongo.init_app(app)
     return mongo
   ```
1. In your [app.py](app.py), display the database connection:   
   ```python
   from flask import Flask
   from backend.db import init_db

   app = Flask(__name__)
   mongo = init_db(app)

   @app.route('/')
   def hello_world():
      return f"DB connection: {mongo.db}"

   if __name__ == '__main__':
      app.run()
   ``` 

## 3. Testing the database connection
1. Create a test class in [tests/backend/test_users.py](tests/backend/test_users.py).
   Connect to the database in [setUpClass()](tests/backend/test_users.py#:~:text=setUpClass)
   ```python
   @classmethod
   def setUpClass(cls):
      app = Flask(__name__)
      cls.mongo = init_db(app)
      cls.db = DbUsers(cls.mongo)
   ``` 
1. Close the database connection in [tearDownClass()](tests/backend/test_users.py#:~:text=tearDownClass)

1. Write tests for the user's CRUD operations.
