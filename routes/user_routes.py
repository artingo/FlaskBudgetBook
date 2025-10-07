from flask import Blueprint, render_template, request, redirect, url_for
from backend.db import dbUsers
from model.user import User

# Create a Blueprint instance
user_bp = Blueprint('users', __name__, url_prefix='/users')

@user_bp.route('/')
def show_users():
    # get all users from the database
    users = dbUsers.read_all()
    # show them in the HTML page
    return render_template('users/index.html', users=users)

@user_bp.route('/create', methods=['GET', 'POST'])
def create():
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
        return redirect(url_for('users.show_users'))

    # all other methods are not allowed
    return "Method not allowed", 405

@user_bp.route('/<user_id>')
def read(user_id):
    user = dbUsers.read(user_id)
    if user is None:
        return f"User with ID '{user_id}' not found", 404
    return render_template('users/read.html', user=user)

@user_bp.route('/update/<user_id>')
def change(user_id):
    user = dbUsers.read(user_id)
    if user is None:
        return f"User with ID '{user_id}' not found", 404
    return render_template('users/update.html', user=user)

@user_bp.route('/update', methods=['POST'])
def update():
    user_id = request.form['_id']
    updated_user = User(request.form['firstname'], request.form['lastname'])
    success = dbUsers.update(user_id, updated_user)

    if not success:
        return f"User with ID '{user_id}' not found", 404

    # redirect to home page
    return redirect(url_for('users.show_users'))

@user_bp.route('/delete', methods=['POST'])
def delete():
    user_id = request.form['_id']
    success = dbUsers.delete(user_id)

    if not success:
        return f"User with ID '{user_id}' not found", 404

    # redirect to home page
    return redirect(url_for('users.show_users'))



