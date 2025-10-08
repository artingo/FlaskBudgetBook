from datetime import datetime
from enum import Enum, auto
from bson import ObjectId

class TransactionType(Enum):
    Income = auto()
    Expense = auto()

class Transaction:
    """
    Represents a single financial transaction (Income or Expense)
    associated with a specific new_user.
    """
    def __init__(self,
                 user_id: ObjectId,
                 kind: int,
                 description: str,
                 category_id: ObjectId,
                 amount: float,
                 date: datetime):
        """
        Initializes a new Transaction object.

        :param user_id: The ID of the associated user.
        :param kind: The nature of the transaction (income or expense).
        :type kind: TransactionType.name
        :param description: The description of the transaction.
        :param category_id: The category of the transaction.
        :param amount: The financial value of the transaction.
        :param date: The date and time the transaction occurred (datetime object).
        """
        self.user_id = user_id
        self.kind = kind
        self.description = description
        self.category_id = category_id
        self.amount = amount
        self.date = date