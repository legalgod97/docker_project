from sqlalchemy import create_engine, Column, Integer, String, Boolean, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime


engine = create_engine("postgresql+psycopg2://postgres:legalisperfect010197@localhost:5432/shop")

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)
    address = Column(String(200), nullable=False)
    wallet = Column(Integer, default=0)
    registration_date = Column(DateTime, default=datetime.now)
    phone_number = Column(String(50), nullable=False)

class Shop(Base):
    __tablename__ = 'shops'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    address = Column(String(200), nullable=False)
    products_list = Column(String(200), default='-')
    product_name = Column(String(255), nullable=False)

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Float, nullable=False)
    in_stock = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey('categories.id'), nullable=False)

    category = relationship('Category', backref='products')

class Order(Base):
    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False)
    address = Column(String(200), nullable=False)
    phone_number = Column(String(50), nullable=False)
    status = Column(String(50), default='Pending')

metadata = Base.metadata