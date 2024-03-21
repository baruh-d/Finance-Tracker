import datetime

class User:
    def  __init__(self, name, ID):
        self._name  = name
        self._ID = ID
        
    @property
    def name(self, value):
        return self._name
    @name.setter
    def name(self, value):
        if isinstance(value, str) and len(value)>0:
            self._name=value
        else:
            raise ValueError("Name must be a non-empty string")
        
    @property
    def ID(self):
        return self._ID
    
    def ID(self, value):
        if  isinstance(value, int) and value >0 :
            self._ID = value
        else:
            raise ValueError('User ID must be a positive integer')
        
    def __str__(self):
        print(f"Name: {self._name}, ID:{self._ID}")
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







