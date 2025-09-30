from flask import Flask, render_template, send_from_directory
from backend.db import init_db
from backend.users import DbUsers

"""
This script handles DB connection and URL routes 
"""
app = Flask(__name__)
mongo = init_db(app)

dbUsers = DbUsers(mongo)
@app.route('/')
def root():
    # get all users from the database
    users = dbUsers.read_all()

    # show them in the HTML page
    return render_template('users/index.html', users=users)

if __name__ == '__main__':
    app.run()