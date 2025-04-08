import pandas as pd
import psycopg2
import os
from datetime import datetime
from dotenv import load_dotenv

# === Load environment variables ===
load_dotenv()

# === Extract ===
def extract_latest_csv(folder_path="data_lake/raw"):
    files = sorted(os.listdir(folder_path))
    latest_file = files[-1]
    filepath = os.path.join(folder_path, latest_file)
    print(f"Extracting from: {filepath}")
    return pd.read_csv(filepath)

# === Transform ===
def transform_data(df):
    df["region"] = df["region"].str.title().str.strip()
    df["product"] = df["product"].str.title().str.strip()

    # Ensure that the timestamp is correctly formatted (if it's a string, convert to datetime)
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors='coerce')
    
    return df

# === Load ===
def load_to_postgres(df):
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
    cur = conn.cursor()

    # Create table if it doesn't exist
    cur.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            order_id TEXT PRIMARY KEY,
            customer_name TEXT,
            region TEXT,
            product TEXT,
            quantity INTEGER,
            unit_price NUMERIC,
            total_price NUMERIC,
            timestamp TIMESTAMP
        )
    """)

    # Insert data in batch using executemany
    insert_query = """
        INSERT INTO sales (order_id, customer_name, region, product, quantity, unit_price, total_price, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (order_id) DO NOTHING
    """
    
    # Create list of tuples for bulk insertion
    data_to_insert = [
        (row["order_id"], row["customer_name"], row["region"], row["product"], row["quantity"],
         row["unit_price"], row["total_price"], row["timestamp"]) for _, row in df.iterrows()
    ]
    
    try:
        cur.executemany(insert_query, data_to_insert)
    except Exception as e:
        print(f"Error during insertion: {e}")

    conn.commit()
    conn.close()
    print(f"Inserted {len(df)} rows into 'sales' table.")

# === Run ===
if __name__ == "__main__":
    df = extract_latest_csv()
    df = transform_data(df)
    load_to_postgres(df)