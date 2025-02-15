# backend/db_setup.py

import sqlite3
import pandas as pd
import os

# Define file paths relative to this file's location
PROCESSED_DATA_PATH = os.path.join(os.path.dirname(__file__), "../YC-Scraper/scraper/ycombinator/scraper/data/processed/processed_data.csv")
DATABASE_PATH = os.path.join(os.path.dirname(__file__), "../data/database.db")

def load_data_to_db():
    """Load data from the processed CSV into SQLite and create indexes."""
    # Load the processed CSV
    data = pd.read_csv(PROCESSED_DATA_PATH)

    # Connect to SQLite database
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Create the 'startups' table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS startups (
        company_id INTEGER PRIMARY KEY,
        company_name TEXT,
        short_description TEXT,
        long_description TEXT,
        batch TEXT,
        status TEXT,
        tags TEXT,
        location TEXT,
        country TEXT,
        year_founded INTEGER,
        num_founders INTEGER,
        founders_names TEXT,
        team_size INTEGER,
        website TEXT,
        cb_url TEXT,
        linkedin_url TEXT
    )
    """)

    # Create indexes on key columns for faster queries
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_company_name ON startups(company_name)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_year_founded ON startups(year_founded)")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_location ON startups(location)")

    # Insert data (replacing any existing table data)
    data.to_sql("startups", conn, if_exists="replace", index=False)

    conn.commit()
    conn.close()
    print("Data loaded and indexes created successfully in the database.")

if __name__ == "__main__":
    load_data_to_db()
