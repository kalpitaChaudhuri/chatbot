from fastapi import FastAPI
from transformers import pipeline
from pydantic import BaseModel
import psycopg2
from transformers import pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
app = FastAPI()

# Model to accept user queries
class QueryRequest(BaseModel):
    query: str

# Database connection setup
def get_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="chatbot_db",
        user="postgres",
        password="123"
    )
    return conn

# Load Hugging Face's summarization pipeline
summarizer = pipeline("summarization")

# Function to summarize the data
def generate_enhanced_response(data):
    # Convert data into a string format
    text = " ".join([str(item) for item in data])  # Simplified for now
    summary = summarizer(text, max_length=150, min_length=50, do_sample=False)
    return summary[0]['summary_text']


# Query Functions for Products and Suppliers

def get_products_by_brand(brand):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM products WHERE brand = %s;', (brand,))
    products = cur.fetchall()
    cur.close()
    conn.close()
    return products

def get_suppliers_by_product_category(category):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM suppliers WHERE product_categories LIKE %s;', ('%' + category + '%',))
    suppliers = cur.fetchall()
    cur.close()
    conn.close()
    return suppliers

def get_product_details(product_name):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM products WHERE name = %s;', (product_name,))
    product_details = cur.fetchone()
    cur.close()
    conn.close()
    return product_details

# FastAPI route to process queries
@app.post("/query/")
async def query_chatbot(request: QueryRequest):
    query = request.query
    
    if "brand" in query:
        brand = query.split("brand")[1].strip()  # Extract brand from the query
        products = get_products_by_brand(brand)
        return {"response": f"Products under {brand}: {products}"}
    
    elif "suppliers" in query and "laptop" in query:  # Example query for laptop suppliers
        suppliers = get_suppliers_by_product_category("laptop")
        return {"response": f"Suppliers providing laptops: {suppliers}"}
    
    elif "details" in query:
        product_name = query.split("details of")[1].strip()  # Extract product name
        product_details = get_product_details(product_name)
        return {"response": f"Details of {product_name}: {product_details}"}
    
    else:
        return {"response": "Sorry, I didn't understand your query."}
