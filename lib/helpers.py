#!/usr/bin/env python3

from db.models import Transaction, Session, get_all_transactions
from collections import defaultdict

def add_transaction():
    """Function to add a transaction."""
    session = Session()

    try:
        # Gather transaction details from user input
        user_id = int(input("Enter user ID: "))
        category_id = int(input("Enter category ID: "))
        description = input("Enter description: ")
        amount = float(input("Enter amount: "))
        transaction_type = input("Enter transaction type (debit/credit): ")
        
        # Create a new transaction object
        transaction = Transaction(
            user_id=user_id,
            category_id=category_id,
            description=description,
            amount=amount,
            transaction_type=transaction_type
        )

        # Add the transaction to the database
        session.add(transaction)
        session.commit()
        print("Transaction added successfully!")

    except Exception as e:
        print(f"Error occurred: {e}")
        session.rollback()

    finally:
        session.close()

def view_transactions():
    """Function to view transactions."""
    session = Session()

    try:
        # Query all transactions from the database
        transactions = session.query(Transaction).all()

        # Print details of each transaction
        for transaction in transactions:
            print(f"Transaction ID: {transaction.id}")
            print(f"User ID: {transaction.user_id}")
            print(f"Category ID: {transaction.category_id}")
            print(f"Description: {transaction.description}")
            print(f"Amount: {transaction.amount}")
            print(f"Transaction Type: {transaction.transaction_type}")
            print()

        if not transactions:
            print("No transactions found.")

        # Call the organizing function with transactions
        organizing_user_transactions_by_month_year(transactions)

    except Exception as e:
        print(f"Error occurred: {e}")

    finally:
        session.close()
    
# function to get the current balance for a user

def get_current_balance(user_id):
    """Calculate the current balance for a user."""
    transactions = get_all_transactions()
    total = 0
    for transaction in transactions:
        # Check if the transaction belongs to the given user
        if transaction.user_id == user_id:
            # Add the amount of the transaction to the total balance
            total += transaction.amount
    return total

def user_transactions_to_dict(transactions):
    """Covert the list of transactions into a dictionary with the transactions IDs as key"""
    transactions = get_all_transactions()
    transation_dict = {trans.id: trans for trans in transactions}
    return transation_dict

def organizing_user_transactions_by_month_year(transactions):
    """Organize transactions by month and year."""
    organized_transactions = defaultdict(list)

    for transaction in transactions:
        month_year = transaction.date.strftime('%Y-%m')
        organized_transactions[month_year].append(transaction)

    for month_year, transactions_list in organized_transactions.items():
        transactions_list.sort(key=lambda x: x.date)

    # Print the organized transactions
    for month_year, transactions_list in organized_transactions.items():
        print(f"Month/Year: {month_year}")
        for transaction in transactions_list:
            print(f"  Transaction ID: {transaction.id}")
            print(f"  User ID: {transaction.user_id}")
            print(f"  Category ID: {transaction.category_id}")
            print(f"  Description: {transaction.description}")
            print(f"  Amount: {transaction.amount}")
            print(f"  Transaction Type: {transaction.transaction_type}")
            print()

    if not organized_transactions:
        print("No transactions found.")





# Function to group transactions by category
# def group_transactions_by_category(transactions):
#     try:
#         grouped_transactions = {}
        
#         for transaction in transactions:
#             if transaction["category"] in grouped_transactions:
#                 grouped_transactions[transaction["category"]]["total_amount"] += transaction["amount"]
#             else:
#                 grouped_transactions[transaction["category"]] = {
#                     "total_amount": transaction["amount"],
#                     "count": 1,
#                     "transactions": [transaction]
#                 }
#         return grouped_transactions
#     except Exception as e:
#         print(f"Error occured when grouping categories:\n{e}")
