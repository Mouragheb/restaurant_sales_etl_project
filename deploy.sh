#!/bin/bash

# Pull the latest changes from GitHub
echo "Pulling the latest changes from GitHub..."
git pull origin main

# Ensure the virtual environment is set up
echo "Setting up the virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run the ETL script
echo "Running the ETL script..."
python3 sales_etl.py

# Optionally restart a service if required (e.g., a web service or a cron job)
# sudo systemctl restart some_service
