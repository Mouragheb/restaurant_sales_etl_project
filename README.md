# Restaurant Sales ETL Project

This project is an ETL (Extract, Transform, Load) pipeline designed for generating fake sales data for a restaurant. The generated data is loaded into a PostgreSQL database, and queries can be run to extract various insights about the sales, such as total sales by product, region, and top customers.

## Features

- **Generate Fake Sales Data**: Generates fake sales records using the `generate_fake_sales.py` script.
- **Extract**: Extracts sales data from CSV files stored in the `data_lake/raw` directory.
- **Transform**: Transforms the data, ensuring all fields are cleaned and formatted.
- **Load**: Loads the transformed data into a PostgreSQL database.
- **Query Sales Data**: Uses `query_sales.py` to execute SQL queries and save the results as CSV files.

## Project Structure
restaurant_sales_etl_project/
├── data_lake/
│   └── raw/
│       └── sales_2025-04-07.csv  # Example generated sales CSV file
├── .env                        # Environment variables (database credentials)
├── generate_fake_sales.py       # Script to generate fake sales data
├── query_sales.py               # Script to run SQL queries and save the results as CSV
├── requirements.txt             # Python dependencies
├── sales_etl.py                 # Main ETL script
├── README.md                   # Project documentation
└── venv/                        # Virtual environment (ignore in git)

## Technologies Used

- Python 3
- PostgreSQL
- Pandas
- psycopg2
- Faker
- python-dotenv

## How to Set Up the Project

### Step 1: Clone the Repository

1. **Clone the repository** to your local machine:

   ```bash
   git clone https://github.com/your-username/restaurant_sales_etl_project.git
   cd restaurant_sales_etl_project
Step 2: Create a Virtual Environment
2.	Create and activate a virtual environment:
   python3 -m venv venv
   source venv/bin/activate  # On macOS/Linux
Step 3: Install Dependencies
3.	Install the required dependencies:
   pip install -r requirements.txt 
Step 4: Set Up the .env File
4.	Create a .env file to store your PostgreSQL credentials. The .env file should contain:
   DB_NAME=mousragheb
   DB_USER=mousragheb
   DB_PASSWORD=12345678
   DB_HOST=localhost
   DB_PORT=5432
Step 5: Generate Fake Sales Data
5.	Generate fake sales data by running the generate_fake_sales.py script. This will generate a CSV file with sales data and store it in the data_lake/raw directory:
    python3 generate_fake_sales.py
Step 6: Run the ETL Process
6.	Run the ETL pipeline to extract, transform, and load the sales data into PostgreSQL:
     python3 sales_etl.py
After running the ETL process, you should see an output like:
     Inserted 500 rows into 'sales' table.
Step 7: Run SQL Queries
7.	Run SQL queries to extract insights from the sales table. You can run pre-defined queries using the query_sales.py script. Each query result will be saved as a CSV file in the data_lake/raw directory.  
     python3 query_sales.py
This will generate CSV files like total_sales_by_product.csv, total_sales_by_region.csv, etc., in the data_lake/raw directory.



Example Output

After running the sales_etl.py script, the following files will be generated:
	•	sales_2025-04-07.csv – This file contains the generated sales data.
	•	total_sales_by_product.csv – Total sales grouped by product.
	•	total_sales_by_region.csv – Total sales grouped by region.
	•	top_5_customers_by_spending.csv – The top 5 customers based on their total spending.
	•	sales_in_2025.csv – All sales data from 2025.


## 🚀 Auto Deployment with GitHub Actions

This project uses **GitHub Actions** to automatically deploy updates to an EC2 instance when changes are pushed to the `main` branch.

### How It Works

1. The **GitHub Actions workflow** (`.github/workflows/deploy.yml`) is triggered on every push to the `main` branch.
2. It:
   - Checks out the latest code
   - Sets up an SSH connection using a secure private key stored in GitHub Secrets (`ETL_KEY`)
   - Connects to your EC2 instance and runs the `deploy.sh` script

### `deploy.sh`

### ```bash
!/bin/bash
echo "Activating virtual environment..."
source venv/bin/activate
echo "Installing requirements..."
pip install -r requirements.txt
echo "Running ETL script..."
python3 sales_etl.py   

This script:
	•	Activates your Python virtual environment
	•	Installs all required packages
	•	Executes your ETL pipeline via sales_etl.py

GitHub Actions Workflow

name: Deploy Project

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout code
      uses: actions/checkout@v2

    - name: Setup SSH key
      run: |
        echo "${{ secrets.ETL_KEY }}" > $HOME/etl-key.pem
        chmod 600 $HOME/etl-key.pem

    - name: Deploy to EC2
      run: |
        ssh -o StrictHostKeyChecking=no -i $HOME/etl-key.pem ubuntu@18.226.34.255 'cd /home/ubuntu/restaurant_sales_etl_project && ./deploy.sh'  

Security Notes
	•	The private SSH key (etl-key.pem) is never committed to the repo and is stored securely as a GitHub Secret named ETL_KEY
	•	The .gitignore ensures .pem files are never tracked
	•	SSH access is limited and secure using key-based authentication

📊 Visual Outputs & Results
etl_script_extract_transform_load.png
postgres_query_output_full_view.png
sales_by_product_query_result.png
sales_by_region_query_result.png
sales_in_2025_csv.png
top_5_customers_by_spending_scv.png
total_sales_by_product_csv.png
total_sales_by_region.png

  License

This project is licensed under the MIT License – see the LICENSE file for details.

Author
	•	Moustafa Ragheb
   GitHub: @Mouragheb

   