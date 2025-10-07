from datetime import datetime, timezone

from bson import ObjectId
from flask import Blueprint, render_template, request, redirect, url_for
from backend.db import mongo
from backend.db_categories import DbCategories
from backend.db_transactions import DbTransactions
from backend.db_users import DbUsers
from model.transaction import TransactionType, Transaction

# Create a Blueprint instance
trans_bp = Blueprint('transactions', __name__, url_prefix='/transactions')

# fixme: delayed initilization
dbUsers = None
dbCategories = None
dbTransactions = None


@trans_bp.route('/')
def show_transactions():
    transactions = get_transactions()
    users = get_users()
    return render_template('transactions/index.html',
                           users=users,
                           transactions=transactions)


@trans_bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        users = get_users()
        categories = get_categories()
        # show new_user creation form
        return render_template('transactions/create.html',
                               users=users,
                               kind=TransactionType,
                               categories=categories)

    if request.method == 'POST':
        transaction = form_to_transaction(request.form)
        get_db_transactions().create(transaction)
        return redirect(url_for('transactions.show_transactions'))

    # all other methods are not allowed
    return "Method not allowed", 405


@trans_bp.route('/<trans_id>')
def read(trans_id):
    transaction = get_db_transactions().read(trans_id)
    if transaction is None:
        return f"Transaction with ID '{trans_id}' not found", 404
    return render_template('transactions/read.html', transaction=transaction)

@trans_bp.route('/update/<trans_id>')
def change(trans_id):
    transaction = get_db_transactions().read(trans_id)
    if transaction is None:
        return f"Category with ID '{trans_id}' not found", 404

    users = get_users()
    categories = get_categories()
    return render_template('transactions/update.html',
                           users=users,
                           kind=TransactionType,
                           categories=categories,
                           transaction=transaction)

@trans_bp.route('/update', methods=['POST'])
def update():
    trans_id = request.form['_id']
    transaction = form_to_transaction(request.form)
    success = get_db_transactions().update(trans_id, transaction)

    if not success:
        return f"Transaction with ID '{trans_id}' not found", 404

    # redirect to home page
    return redirect(url_for('transactions.show_transactions'))

@trans_bp.route('/delete', methods=['POST'])
def delete():
    trans_id = request.form['_id']
    success = get_db_transactions().delete(trans_id)

    if not success:
        return f"Transaction with ID '{trans_id}' not found", 404

    # redirect to home page
    return redirect(url_for('transactions.show_transactions'))

# =============================================================================
def get_users():
    global dbUsers
    if (dbUsers is None):
        dbUsers = DbUsers(mongo)
    return dbUsers.read_all()


def get_categories():
    global dbCategories
    if (dbCategories is None):
        dbCategories = DbCategories(mongo)
    return dbCategories.read_all()


def get_db_transactions():
    global dbTransactions
    if (dbTransactions is None):
        dbTransactions = DbTransactions(mongo)
    return dbTransactions


def get_transactions():
    dbTransactions = get_db_transactions()
    return dbTransactions.read_all()


def form_to_transaction(form):
    transaction = Transaction(
        ObjectId(form['user_id']),
        int(form['kind']),
        form['description'],
        ObjectId(form['category_id']),
        float(form['amount']),
        datetime.now(timezone.utc)
    )
    return transaction
