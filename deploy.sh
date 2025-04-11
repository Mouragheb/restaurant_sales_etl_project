#!/bin/bash

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing requirements..."
pip install -r requirements.txt

echo "Running ETL script..."
python3 sales_etl.py