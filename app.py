from flask import render_template, request, redirect, url_for
from backend.db import mongo
from backend.db_categories import DbCategories
from backend.db_users import DbUsers
from model.user import User
from . import create_app

"""
This script handles DB connection and URL routes 
"""
app = create_app()
dbUsers = DbUsers(mongo)
dbCategories = DbCategories(mongo)

@app.route('/')
def root():
    return render_template("index.html")


@app.route('/users')
def show_users():
    # get all users from the database
    users = dbUsers.read_all()

    # show them in the HTML page
    return render_template('users/index.html', users=users)

@app.route('/users/create', methods=['GET', 'POST'])
def users_create():
    if request.method == 'GET':
        # show new_user creation form
        return render_template('users/create.html')

    if request.method == 'POST':
        new_user = User(request.form['firstname'], request.form['lastname'])
        user_id = dbUsers.create(new_user)

        # if new_user with this name already exists, return error code 409
        if user_id is None:
            return f"User with name '{new_user.firstname + ' ' + new_user.lastname}' already exists", 409

        # redirect to home page
        return redirect(url_for('show_users'))

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
    updated_user = User(request.form['firstname'], request.form['lastname'])
    success = dbUsers.update(user_id, updated_user)

    if not success:
        return f"User with ID '{user_id}' not found", 404

    # redirect to home page
    return redirect(url_for('show_users'))

@app.route('/users/delete', methods=['POST'])
def users_delete():
    user_id = request.form['_id']
    success = dbUsers.delete(user_id)

    if not success:
        return f"User with ID '{user_id}' not found", 404

    # redirect to home page
    return redirect(url_for('show_users'))
# =============================================================================


@app.route('/categories')
def show_categories():
    categories = dbCategories.read_all()
    return render_template('categories/index.html', categories=categories)

@app.route('/categories/create', methods=['GET', 'POST'])
def categories_create():
    if request.method == 'GET':
        # show new_user creation form
        return render_template('categories/create.html')

    if request.method == 'POST':
        description = request.form['description']
        new_category = dbCategories.create(description)

        # if category already exists, return error code 409
        if new_category is None:
            return f"Category '{description}' already exists", 409

        # redirect to home page
        return redirect(url_for('show_categories'))

    # all other methods are not allowed
    return "Method not allowed", 405

@app.route('/categories/<cat_id>')
def categories_read(cat_id):
    category = dbCategories.read(cat_id)
    if category is None:
        return f"Category with ID '{cat_id}' not found", 404
    return render_template('categories/read.html', category=category)

@app.route('/categories/update/<cat_id>')
def categories_change(cat_id):
    category = dbCategories.read(cat_id)
    if category is None:
        return f"Category with ID '{cat_id}' not found", 404
    return render_template('categories/update.html', category=category)

@app.route('/categories/update', methods=['POST'])
def categories_update():
    _id = request.form['_id']
    description = request.form['description']
    success = dbCategories.update(_id, description)

    if not success:
        return f"Category with ID '{_id}' not found", 404

    # redirect to home page
    return redirect(url_for('show_categories'))

@app.route('/categories/delete', methods=['POST'])
def categories_delete():
    cat_id = request.form['_id']
    success = dbCategories.delete(cat_id)

    if not success:
        return f"User with ID '{id}' not found", 404

    # redirect to home page
    return redirect(url_for('show_categories'))


if __name__ == '__main__':
    app.run(debug=True)
