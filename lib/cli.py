from helpers import add_transaction, view_transactions, get_current_balance

if __name__ == "__main__":
    while True:
        print("1. Add a transaction")
        print("2. View all transactions")
        print("3. Organize transactions")
        print("4. Get current balance")
        print("5. Quit the program")
        
        option = input("Enter your option (1/2/3/4/5): ")

        if option == "1":
            add_transaction()
        elif option == "2":
            view_transactions()
        elif option == "3":
            print("Organizing transactions...")
        elif option == "4":
            user_id = int(input("Enter user ID: "))
            balance = get_current_balance(user_id)
            print(f"Current balance for user {user_id}: {balance}")
        elif option == "5":
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid Option! Please enter 1, 2, 3, 4, or 5.")