from datetime import datetime
from enum import Enum, auto

from model.category import Category


class TransactionType(Enum):
    INCOME = auto()
    EXPENSE = auto()

class Transaction:
    """
    Represents a single financial transaction (Income or Expense)
    associated with a specific user.
    """
    def __init__(self,
                 user_id: str,
                 kind: TransactionType,
                 category: Category,
                 amount: float,
                 date: datetime):
        """
        Initializes a new Transaction object.

        :param user_id: The unique ID of the user.
        :param kind: The nature of the transaction.
        :param category: The category of the transaction.
        :param amount: The financial value of the transaction.
        :param date: The date and time the transaction occurred (datetime object).
        """
        self.user_id = user_id
        self.kind = kind
        self.category = category
        self.amount = amount
        self.date = date


