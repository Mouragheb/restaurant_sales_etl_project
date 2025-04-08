import pandas as pd
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Connect to PostgreSQL database
def connect_db():
    dbname = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")

    conn = psycopg2.connect(
        dbname=dbname,
        user=user,
        password=password,
        host=host,
        port=port
    )
    return conn

# Function to execute a SQL query and save the result as CSV
def query_to_csv(query, output_filename):
    conn = connect_db()
    df = pd.read_sql_query(query, conn)
    conn.close()

    # Ensure the 'data_lake/raw' directory exists
    os.makedirs("data_lake/raw", exist_ok=True)

    # Save the DataFrame to a CSV file
    df.to_csv(f"data_lake/raw/{output_filename}", index=False)
    print(f"Query results saved to data_lake/raw/{output_filename}")

# Queries
queries = [
    {
        "query": """
            SELECT product, SUM(total_price) AS total_sales
            FROM sales
            GROUP BY product
            ORDER BY total_sales DESC;
        """,
        "filename": "total_sales_by_product.csv"
    },
    {
        "query": """
            SELECT region, SUM(total_price) AS total_sales
            FROM sales
            GROUP BY region
            ORDER BY total_sales DESC;
        """,
        "filename": "total_sales_by_region.csv"
    },
    {
        "query": """
            SELECT customer_name, SUM(total_price) AS total_spent
            FROM sales
            GROUP BY customer_name
            ORDER BY total_spent DESC
            LIMIT 5;
        """,
        "filename": "top_5_customers_by_spending.csv"
    },
    {
        "query": """
            SELECT * FROM sales
            WHERE timestamp BETWEEN '2025-01-01' AND '2025-12-31';
        """,
        "filename": "sales_in_2025.csv"
    }
]

# Run the queries and save the results as CSV files
for query in queries:
    query_to_csv(query["query"], query["filename"])