import pandas as pd
import psycopg2
import os
from datetime import datetime
from dotenv import load_dotenv

# === Load environment variables ===
load_dotenv()

# === Extract ===
def extract_latest_csv(folder_path="data_lake/raw"):
    # Sort the files by their name in reverse order
    files = sorted([f for f in os.listdir(folder_path) if f.endswith('.csv') and 'sales_' in f], reverse=False)
    print(f"Available files: {files}")  # Debug print to check which files are found
    if not files:
        print("No valid CSV files found.")
        return None
    latest_file = files[0]
    filepath = os.path.join(folder_path, latest_file)
    print(f"Extracting from: {filepath}")  # Show which file is being extracted
    return pd.read_csv(filepath)
if __name__ == "__main__":
    df = extract_latest_csv()
    print(df.head())  # This will print the first few rows of the extracted data

# === Transform ===
def transform_data(df):
    # Check if 'region' and 'product' columns exist
    if 'region' not in df.columns:
        raise KeyError("'region' column is missing from the CSV file")
    if 'product' not in df.columns:
        raise KeyError("'product' column is missing from the CSV file")
    
    # Clean up 'region' and 'product' columns
    df["region"] = df["region"].str.title().str.strip()
    df["product"] = df["product"].str.title().str.strip()

    # Ensure that the timestamp is correctly formatted (if it's a string, convert to datetime)
    if 'timestamp' in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors='coerce')
    else:
        raise KeyError("'timestamp' column is missing from the CSV file")
    
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
    try:
        df = extract_latest_csv()
        df = transform_data(df)
        load_to_postgres(df)
    except KeyError as e:
        print(f"Missing expected column: {e}")


# Update the print statement to test the change
print("ETL script executed successfully with the updated CI/CD pipeline!")
print("Test Github auto deployment")
