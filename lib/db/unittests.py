#!/usr/bin/env python3

import unittest
from datetime import datetime
from collections import defaultdict

# Import the functions to be tested
from models import get_all_transactions
from helpers import user_transactions_to_dict, organizing_user_transactions_by_month_year

class TestTransactionFunctions(unittest.TestCase):
    def test_user_transactions_to_dict(self):
        # Mock transactions data for testing
        transactions = [
            {"id": 1, "date": datetime(2023, 1, 15), "amount": 100.0},
            {"id": 2, "date": datetime(2023, 2, 20), "amount": 150.0},
            # Add more mock data as needed
        ]
        
        # Mock the get_all_transactions function
        def mock_get_all_transactions():
            return transactions

        # Patch the get_all_transactions function to return mock data
        with unittest.mock.patch("db.models.get_all_transactions", side_effect=mock_get_all_transactions):
            # Call the function to be tested
            transaction_dict = user_transactions_to_dict()

        # Check if the output is as expected
        expected_output = {1: transactions[0], 2: transactions[1]}  # Assuming transactions have unique IDs
        self.assertEqual(transaction_dict, expected_output)

    def test_organizing_user_transactions_by_month_year(self):
        # Mock transaction dictionary for testing
        transaction_dict = {
            1: {"id": 1, "date": datetime(2023, 1, 15), "amount": 100.0},
            2: {"id": 2, "date": datetime(2023, 2, 20), "amount": 150.0},
            # Add more mock data as needed
        }

        # Call the function to be tested
        organized_transactions = organizing_user_transactions_by_month_year(transaction_dict)

        # Check if the output is as expected
        expected_output = defaultdict(list)
        expected_output["2023-01"].append(transaction_dict[1])
        expected_output["2023-02"].append(transaction_dict[2])
        # Add more expected output as needed

        self.assertEqual(organized_transactions, expected_output)

    # Add more test cases as needed

if __name__ == "__main__":
    unittest.main()
