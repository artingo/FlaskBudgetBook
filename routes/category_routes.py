from flask import Blueprint, render_template, request, redirect, url_for
from backend.db import  dbCategories

# Create a Blueprint instance
cat_bp = Blueprint('categories', __name__, url_prefix='/categories')

@cat_bp.route('/')
def show_categories():
    categories = dbCategories.read_all()
    return render_template('categories/index.html', categories=categories)

@cat_bp.route('/create', methods=['GET', 'POST'])
def create():
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
        return redirect(url_for('categories.show_categories'))

    # all other methods are not allowed
    return "Method not allowed", 405

@cat_bp.route('/<cat_id>')
def read(cat_id):
    category = dbCategories.read(cat_id)
    if category is None:
        return f"Category with ID '{cat_id}' not found", 404
    return render_template('categories/read.html', category=category)

@cat_bp.route('/update/<cat_id>')
def change(cat_id):
    category = dbCategories.read(cat_id)
    if category is None:
        return f"Category with ID '{cat_id}' not found", 404
    return render_template('categories/update.html', category=category)

@cat_bp.route('/update', methods=['POST'])
def update():
    _id = request.form['_id']
    from model.category import Category
    updated_category = Category(request.form['description'])
    success = dbCategories.update(_id, updated_category)

    if not success:
        return f"Category with ID '{_id}' not found", 404

    # redirect to home page
    return redirect(url_for('categories.show_categories'))

@cat_bp.route('/delete', methods=['POST'])
def delete():
    cat_id = request.form['_id']
    success = dbCategories.delete(cat_id)

    if not success:
        return f"User with ID '{id}' not found", 404

    # redirect to home page
    return redirect(url_for('categories.show_categories'))

