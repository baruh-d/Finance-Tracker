#import necessary libraries
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm  import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError
from passlib.hash import bcrypt #for password encryption
import datetime

#define the base class for all tables in the database
Base = declarative_base()
#define the user tabla in the database
class User(Base):
    #table name
    __tablename__ = "users"
    #defining the columns for the table
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(64), nullable=False)
    email = Column(String(20), unique=True, index=True)
    password_hash = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now())
    last_login = Column(DateTime)
    updated_at = Column(DateTime, onupdate=datetime.datetime.now())

    #defining a method to set the user's password using bcrypt for password encryption
    def set_password(self, password, user_id):
        """set the user password using bcrypt password encryprion"""
        salt = bcrypt.gensalt(rounds=10)
        #concatenate password with the user ID
        salted_password = str(user_id) + '@' + password
        #hash the slated password
        self.password_hash = bcrypt.hashpw(salted_password.encode('utf-8'), salt)
    #defining a method to check if the entered password is correct or not
    def check_password(self, password):
        #spliting the salted password into two parts: user ID and password
        return bcrypt.verify(password.encode('utf-8'), self.password_hash)  
    
    #updating  the login time everytime when someone logs in
    @staticmethod
    def update_last_login(session, user_id):
        #get the user object from the current session
        user = session.query(User).filter_by(id=user_id).first()
        #update the last login attribute of the user
        user.last_login = datetime.datetime.now()
        #commit the changes to the database
        try:
            session.commit()
        except Exception as e:
            print("Error while updating the last login")
            raise e
        
    #retrieving user  information based on the given email address
    @staticmethod
    def get_user_by_email(db_session, email):
        return db_session.query(User ).filter_by(email=email).first()        
        
class Transactions(Base):
    """Model representing transactions made."""
    #table name
    __tablename__ = 'transactions'
    #columns for transactions table
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    amount = Column(float, nullable=False)
    date = Column(DateTime, default=datetime.datetime.now())
    description = Column(String(255))
    
    #Relationship to the user model
    user = relationship("User", back_populates="transactions")    
    
class Category(Base):
    """Model representing categories for expenses."""
    #table name
    __tablename__ = 'categories'
    #columns for categories table
    id = Column(Integer, primary_key=True, autoincrement=True)
    label = Column(String(30), nullable=False)
    user_id = Column(Integer(ForeignKey('users.id')))
    
    #relationship to user model
    user = relationship("User", backref='categories', lazy='joined')

# Connect to the database
engine = create_engine('sqlite:///finance_tracker.db', echo=True)
Session = sessionmaker(bind=engine)

#function to add user to the users table in the db
def add_user(name, email, password):
    """Add a new user to the users table in the database.
    create a new user object with given name, email and hashed password"""
    try:
        existing_user = User.query.filter_by(email=email).first()
        if existing_user is not None:
            raise ValueError("Email already exists.")
        #create new user object    
        user = User(name=name, email=email)
        user.set_password(password, user.id)  #hashes the password before storing
        #establishing connection with db session
        db_session = Session()
        #adding new user object to database session
        db_session.add(user)
        #commit the transaction to the database, saving new user
        db_session.commit()
        #retrun newly created user object
        return user
    #if error occurs, rollback the transaction and re-raise the exception
    except IntegrityError  as e:
        print(f"An error occurred while adding a new user:\n{e}")

def get_all_users():
    """Get all users from the users table."""
    #establish connection to db
    db_session = Session()
    #query all user objects and the query is ordered by the created_at attribute sorting based on when they were created
    users = db_session.query(User).order_by(User.created_at)
    #once query is executed, the db coonection is closed
    db_session.close()
    #function returns the queried users
    return users

def delete_user(user_id):
    """Delete a user with given user ID from the users table."""
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

def authenticate_user(email, password):
    """Authenticate a user by checking their  email and password against the 
    ones stored in the database."""
    #Query the user with the provided email
    user = User.get_user_by_email(Session(), email())
    #check if user exists
    if user and user.check_password(password):
        #update last login time of the user
        user.update_last_login = datetime.datetime.now()
        #save the change to the user's information
        Session().commit()
        #return the logged-in user
        return user
    else:
        return "Invalid Email or Password"
       
        

    