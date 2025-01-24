import sqlite3
import pandas as pd

# Define the file paths
PROCESSED_DATA_PATH = "YC-Scraper/scraper/ycombinator/scraper/data/processed/scraped_data.csv"
DATABASE_PATH = "data/database.db"

def load_data_to_db():
    """Load data from the processed CSV file into SQLite."""
    # Load the processed CSV
    data = pd.read_csv(PROCESSED_DATA_PATH)

    # Establish SQLite connection
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Create table if it doesn't exist
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
    
    # Insert data into the database
    data.to_sql("startups", conn, if_exists="replace", index=False)

    conn.commit()
    conn.close()
    print("Data loaded successfully into the database.")
