from sqlalchemy.orm import Session
from backend.database import SessionLocal, Product, Supplier

# Create a new database session
db: Session = SessionLocal()

# Sample suppliers
supplier1 = Supplier(name="Tech Distributors", contact_info="tech@example.com", product_categories_offered="Electronics")
supplier2 = Supplier(name="Fashion Hub", contact_info="fashion@example.com", product_categories_offered="Clothing")

db.add_all([supplier1, supplier2])
db.commit()

# Sample products
product1 = Product(name="Laptop", brand="Dell", price=75000, category="Electronics", description="15-inch laptop", supplier_id=supplier1.id)
product2 = Product(name="T-shirt", brand="Nike", price=1200, category="Clothing", description="Cotton T-shirt", supplier_id=supplier2.id)

db.add_all([product1, product2])
db.commit()

db.close()
print("Sample data added successfully!")
