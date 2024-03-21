from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm  import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from passlib.hash import bcrypt #for password encryption
import datetime

Base = declarative_base()
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    email = Column(String(12), unique=True, index=True)
    password_hash = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now.today)
    updated_at = Column(DateTime, onupdate=datetime.datetime.now.today)
    
class Transactions(Base):
    """Model representing transactions made."""
    __tablename__ = 'transactions'
    id = Column(Integer, primary_key=True)
    user_id = (Integer(ForeignKey('users.id')), )
    date = Column(DateTime, default=datetime.datetime.now())
    description = Column(String(255))
    user = relationship("User", back_populates="transactions")    
    
class Category(Base):
    """Model representing categories for expenses."""
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    label = Column(String(30), nullable=False)
    user_id = Column(Integer(ForeignKey('users.id')))
    user = relationship("User", backref='categories', lazy='joined')

# Connect to the database
engine = create_engine('sqlite:///finance_tracker.db', echo=True)
Session = sessionmaker(bind=engine)

def add_user(name, email, password):
    """Add a new user to the users table in the database."""
    user = User(name=name, email=email, password_hash=bcrypt.encrypt(password))
    db_session = Session()
    db_session.add(user)
    db_session.commit()
    return user

def get_all_users():
    """Get all users from the users table."""
    db_session = Session()
    users = db_session.query(User).order_by(User.created_at)
    db_session.close()
    return users

def delete_user(user_id):
    """Delete a user with given user ID from the users table."""
    db_session = Session()
    user = db_session.query(User).filter_by(id=user_id).first()
    if not user:
        raise ValueError("No user found with that ID.")
    db_session.delete(user)
    db_session.commit()

def authenticate_user(email, password):
    """Authenticate a user by checking their  email and password against the 
    ones stored in the database."""
    db_session = Session()
    user = db_session.query(User).filter_by(email=email).first()
    if user is None or bcrypt.checkpw(password.encode('utf-8'), user.password_hash) == False:
        return None
    else:
        return user
    