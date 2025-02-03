from sqlalchemy import create_engine, Column, Integer, String, DECIMAL, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# PostgreSQL connection URL
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123@localhost/chatbot_db"  # Update with your details

# Create the engine that will interact with PostgreSQL
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Define the base class for your models
Base = declarative_base()

# Define a model (table) for 'products'
class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    brand = Column(String)
    price = Column(DECIMAL)
    category = Column(String)
    description = Column(Text)
    supplier_id = Column(Integer)

# Define a model (table) for 'suppliers'
class Supplier(Base):
    __tablename__ = 'suppliers'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    contact_info = Column(Text)
    product_categories = Column(Text)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Function to create all tables in the database
def create_tables():
    Base.metadata.create_all(bind=engine)

# Function to get a session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
