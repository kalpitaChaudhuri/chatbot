from fastapi import FastAPI
from transformers import pipeline
from pydantic import BaseModel
import psycopg2

app = FastAPI()

# Model to accept user queries
class QueryRequest(BaseModel):
    query: str

# Database connection setup
def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="chatbot_db",
        user="postgres",
        password="123"
    )

# Function to summarize the data
def generate_enhanced_response(data):
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
    text = " ".join([str(item) for item in data])  # Convert data into a string
    summary = summarizer(text, max_length=150, min_length=50, do_sample=False)
    return summary[0]['summary_text']

# Query Functions for Products and Suppliers
def get_products_by_brand(brand):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM products WHERE LOWER(brand) = LOWER(%s);", (brand,))
            return cur.fetchall()

def get_suppliers_by_product_category(category):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM suppliers WHERE LOWER(product_categories) LIKE LOWER(%s);", ('%' + category + '%',))
            return cur.fetchall()

def get_product_details(product_name):
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM products WHERE LOWER(name) = LOWER(%s);", (product_name,))
            return cur.fetchone()

# FastAPI GET route for the root URL
@app.get("/")
def read_root():
    return {"message": "Welcome to the chatbot backend!"}

# FastAPI POST route to process queries
@app.post("/query/")
async def query_chatbot(request: QueryRequest):
    query = request.query.lower()
    
    if "brand" in query:
        brand = query.split("brand")[-1].strip()
        products = get_products_by_brand(brand)
        return {"response": f"Products under {brand}: {products}"}

    elif "suppliers" in query and "laptop" in query:
        suppliers = get_suppliers_by_product_category("laptop")
        return {"response": f"Suppliers providing laptops: {suppliers}"}

    elif "details of" in query:
        product_name = query.split("details of")[-1].strip()
        product_details = get_product_details(product_name)
        return {"response": f"Details of {product_name}: {product_details}"}

    else:
        return {"response": "Sorry, I didn't understand your query."}
