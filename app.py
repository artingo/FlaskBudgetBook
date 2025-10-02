from flask import Flask, render_template, request, redirect, url_for
from jinja2.runtime import str_join

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

@app.route('/users/create', methods=['GET', 'POST'])
def users_create():
    if request.method == 'GET':
        # show user creation form
        return render_template('users/create.html')

    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        user_id = dbUsers.create(firstname, lastname)

        # if user with this name already exists, return error code 409
        if user_id is None:
            return f"User with name '{firstname + ' ' + lastname}' already exists", 409

        # redirect to home page
        return redirect(url_for('root'))

    # all other methods are not allowed
    return "Method not allowed", 405

@app.route('/users/<user_id>')
def users_read(user_id):
    user = dbUsers.read(user_id)
    if user is None:
        return f"User with ID '{user_id}' not found", 404
    return render_template('users/read.html', user=user)

@app.route('/users/update/<user_id>')
def users_change(user_id):
    user = dbUsers.read(user_id)
    if user is None:
        return f"User with ID '{user_id}' not found", 404
    return render_template('users/update.html', user=user)

@app.route('/users/update', methods=['POST'])
def users_update():
    user_id = request.form['_id']
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    success = dbUsers.update(user_id, firstname, lastname)

    if not success:
        return f"User with ID '{user_id}' not found", 404

    # redirect to home page
    return redirect(url_for('root'))

@app.route('/users/delete', methods=['POST'])
def users_delete():
    user_id = request.form['_id']
    success = dbUsers.delete(user_id)

    if not success:
        return f"User with ID '{user_id}' not found", 404

    # redirect to home page
    return redirect(url_for('root'))

# ToDo: separate files for entity routes

if __name__ == '__main__':
    app.run()