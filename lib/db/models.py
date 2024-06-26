#!/usr/bin/env python3

#import necessary libraries
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, ForeignKey, func
from sqlalchemy.orm  import relationship, sessionmaker
from sqlalchemy.orm import declarative_base
from sqlalchemy.exc import IntegrityError
import bcrypt #for password encryption 
from typing import List
import datetime

#define the base class for all tables in the database
Base = declarative_base()


#define the user tabla in the database
class User(Base):
    #table name
    __tablename__: str = "users"
    #defining the columns for the table
    id: int = Column(Integer, primary_key=True, autoincrement=True)
    name:str = Column(String(64), nullable=False)
    email:str = Column(String(20), unique=True, index=True)
    password_hash:str = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now())
    last_login = Column(DateTime, default=datetime.datetime.now())
    updated_at = Column(DateTime, default=datetime.datetime.now, onupdate=datetime.datetime.now())
    
    #relationship to transactions model (one to many relationship)
    transactions = relationship("Transaction", back_populates="user", uselist=True)
    
    def set_password(self, password):
        """Set the user password using bcrypt password encryption."""
        salt = bcrypt.gensalt(rounds=10)
        # Concatenate password with the user ID
        salted_password = str(self.id) + '@' + password
        # Hash the salted password
        self.password_hash = bcrypt.hashpw(salted_password.encode('utf-8'), salt)

    #method to check if the entered password is correct or not
    def check_password(self, password):
        # Concatenate password with the user ID
        salted_password = str(self.id) + '@' + password
        # Verify the password
        return bcrypt.verify(salted_password.encode('utf-8'), self.password_hash.encode('utf-8'))

        #updating  the login time everytime when someone logs in
   
class Transaction(Base):
    """Model representing transactions made."""
    #table name
    __tablename__: str = 'transaction'
    #columns for transactions table
    id:int = Column(Integer, primary_key=True, autoincrement=True)
    user_id:int = Column(Integer, ForeignKey('users.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))  # Adding category_id column
    amount:float = Column(Float, nullable=False)
    date = Column(DateTime, default=datetime.datetime.now())
    description:str = Column(String(255), nullable=True)
    transaction_type:str = Column(String(10)) #debit or credit
    
    #Relationship to the user model (one to many relationship)
    user = relationship("User", back_populates="transactions")    
    
    # Relationship to the Category model (many-to-one relationship)
    category = relationship("Category", back_populates="transactions") 
    
class Category(Base):
    """Model representing categories for expenses."""
    #table name
    __tablename__: str = 'categories'
    #columns for categories table
    id:int = Column(Integer, primary_key=True, autoincrement=True)
    label:str = Column(String(30), nullable=False)
    user_id:int = Column(Integer, ForeignKey('users.id'))
    
    #relationship to user model
    user = relationship("User", backref='categories', lazy='joined')
    
    # Relationship to the Transaction model (one-to-many relationship)
    transactions = relationship("Transaction", back_populates="category")

# Connect to the database
engine = create_engine('sqlite:///finance_tracker.db', echo=True)
Session = sessionmaker(bind=engine)

#function to add user to the users table in the db
def add_user(name, email, password):
    """Add a new user to the users table in the database.
    create a new user object with given name, email and hashed password"""
    try:
        #establishing connection with db session
        db_session = Session()
        existing_user = db_session.query(User).filter_by(email=email).first()
        if existing_user is not None:
            raise ValueError("Email already exists.")
        #create new user object    
        user = User(name=name, email=email)
        #adding new user object to database session
        db_session.add(user)
        #commit the transaction to the database, saving new user
        db_session.commit()
        user.set_password(password=password, user_id=user.id)  #hashes the password before storing
        db_session.commit()
        #retrun newly created user object
        return user
    #if error occurs, rollback the transaction and re-raise the exception
    except IntegrityError  as e:
        print(f"An error occurred while adding a new user:\n{e}")

def get_all_users():
    """Get all users from the users table."""
    try:
        #establish connection to db
        db_session = Session()
        #query all user objects and the query is ordered by the created_at attribute sorting based on when they were created
        users = db_session.query(User).order_by(User.created_at).all()
        #once query is executed, the db coonection is closed
        db_session.close()
        #function returns the queried users
        return users
    except Exception as e:
        print(f'Error occured when fetching users:\n{e}')

def get_user_by_email(email):
    """Retrieve user information based on the given email address."""
    try:
        db_session = Session()
        user = db_session.query(User).filter_by(email=email).first()
        db_session.close()
        return user
    except Exception as e:
        print(f"Error while retrieving user by email:\n{e}")
        return None

def update_last_login(user_id):
    """Update the last login time for the user."""
    try:
        db_session = Session()
        user = db_session.query(User).filter_by(id=user_id).first()
        user.last_login = datetime.datetime.now()
        db_session.commit()
        db_session.close()
    except Exception as e:
        db_session.rollback()
        print(f"Error while updating the last login:\n{e}")
        
def delete_user(user_id):
    """Delete a user with given user ID from the users table."""
    try:
        #create new db session
        db_session = Session()
        #query  for user with matching user_id 
        user = db_session.query(User).filter_by(id=user_id).first()
        #if no user is found withe given ID, raise ValueError
        if not user:
            raise ValueError("No user found with that ID.")
        #delete user from db
        db_session.delete(user)
        #commit changes to db
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        print(f"Error when deleting user:\n{e}")
        
def authenticate_user(email, password):
    """Authenticate a user by checking their  email and password against the 
    ones stored in the database."""
    try:
        #Query the user with the provided email
        user = get_user_by_email(Session(), email)
        #check if user exists
        if user and user.check_password(password):
            #update last login time of the user
            update_last_login(Session(), user.id)
            #save the change to the user's information
            db_session = Session()
            db_session.commit()
            #return the logged-in user
            return user
        else:
            return "Invalid Email or Password"
    except Exception as e:
        print(f"Error occured during authentication:\n{e}")
    

def get_all_transactions():
    """Get all transactions from the transactions table."""
    #create new db session
    db_session = Session()
    #Use the query function to select all records from the transactions table
    try:
        #Execute the query and fetch all results
        result = db_session.query(Transaction).order_by(Transaction.date.desc()).all()
    finally:
        db_session.close()
        return result

def delete_transaction(transaction_id):
    """Delete a specific transaction from the transactions table."""
    #use the remove method on the session object to remove the record with the given id from the transactions table
    try:
        db_session = Session()
        trans = db_session.query(Transaction).filter_by(id=transaction_id).first()
        #if no transaction is found by that transaction_id raise ValueError
        if not trans:
            raise ValueError("No transaction found with that transaction_ID")
        #remove transaction from database
        db_session.delete(trans)
        #commit changes to db
        db_session.commit()
    except Exception as e:
        #Rollback transaction if error occurs
        db_session.rollback()
        print(f"Error occured when deleting transaction:\n{e}")
        
def add_category(user_id, label):
    """Add a category to the category table"""
    try:
        #establish db session
        db_session = Session()
        #create new category object
        category = Category(user_id=user_id, label=label)
        #add new category object to session
        db_session.add(category)
        #commit changes
        db_session.commit()
        #return newly created category
        return category
    except Exception as e:
        db_session.rollback()
        print(f"Error occured when adding category:\n{e}")
            
def select_category(category_id):
    """Select category by its ID"""
    try:
        db_session = Session()
        #execute query and fetch the result
        category = db_session.query(Category).filter_by(id=category_id).first().all()
        #close the db session
        db_session.close()
        #return selected category
        return category
    except Exception as e:
        print(f"Error occured when selecting category:\n{e}")
        
def group_category():
    """Group categories by user"""
    try:
        db_session = Session()
        #query the db for the number of categories grouped by user_id for each user
        #func.count is used to count the number of categories
        result = db_session.query(Category.user_id, func.count(Category.id)).group_by(Category.user_id).all()
        #close db session
        db_session.close()
        #Return the result of the query
        return result
    except Exception as e:
        print(f"Error occured when grouping categories:\n{e}")
        
# Main code execution
if __name__ == "__main__":
    Base.metadata.create_all(engine)

    
    