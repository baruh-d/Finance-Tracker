import datetime

class User:
    def  __init__(self, name, ID):
        self._name  = name
        self._ID = ID
    pass

class Transactions:
    def  __init__(self):
        self.transactions_list=[]
    
    def add_transaction(self, user, amount, date, description, category):
        if isinstance(user,User) and isinstance(amount, (int, float)):
            transaction = {"user": user._name ,"Amount": amount , "Date": date , "Decription": description ,  "Categoty": category}
            self.transactions_list.append(transaction)
        else:
            print("Invalid input")
            
    def get_all_transactions(self):
        return self.transactions_list
       
    def total_transactions_for_user(self, user):
        user_transactions = [transaction["Amount"] for transaction in self.transactions_list if transaction["user"] == user._name]
        return sum(user_transactions)
    pass


class Categories:
    def  __init__(self):
        self.categories=[]
        
    def add_category(self, category):
        self.categories.append(category)
        
    def remove_category(self, category):
        try:
            self.categories.remove(category)    
        except ValueError as e: 
            print(f"Category {category} does not exist.")    
            
    def show_categories(self):
        return self.categories

    pass








#Testing the code
# u1 = User('John', '001')
# u2 = User('Jane', '002')
# t = Transactions()
# t.add_transaction(u1, 50)
# t.add_transaction(u2, 75.50)
# print(t.get_all_transactions())
'''
# Testing the code
u1 = User('John Doe', '001')
u2 = User('Jane Smith','002')
t = Transactions()
c = Categories()

print(u1.get_name()) # John Doe
print(u2.get_name()) # Jane Smith

t.add_transaction(u1, 50.50, datetime.now(), "Gas", "Food")
t.add_transaction(u1, -30,'2021-04-06', "Coffee", "Entertainment")
t.show_transactions(u1)

c.add_category("Food")
c.add_category("Transportation")
c.show_categories()

print(t.total_transactions_for_user(u1)) #  80.0
print(t.total_transactions_for_user(u2)) #  0.0
'''