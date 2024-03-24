#!/usr/bin/env python3

from db.models import get_all_transactions
from collections import defaultdict
def user_transactions_to_dict(transactions):
    """Covert the list of transactions into a dictionary with the transactions IDs as key"""
    transactions = get_all_transactions()
    transation_dict = {trans.id: trans for trans in transactions}
    return transation_dict

def organizing_user_transactions_by_month_year(transaction_dict):
    #creating a defaultdict to organize transactions by month_year
    organized_transactions  = defaultdict(list)
    #iterating through the transactions extracting month and year and groupin gthe transactions
    for transaction in transaction_dict.items():
        month_year = transaction.date.strftime('%Y-%m')
        organized_transactions[month_year].append(transaction)
    #sort transactions within the month_year group by date
    for month_year, transactions_list in organized_transactions.items():
        transactions_list.sort(key=lambda x: x.date)
    return organized_transactions