import pandas as pd
import sqlite3

# Path to CSV file
csv_file = "data/raw/scraped_data.csv"
db_file = "data/database.db"

# Read CSV and convert to SQLite
def create_database():
    df = pd.read_csv(csv_file)
    conn = sqlite3.connect(db_file)
    df.to_sql("startups", conn, if_exists="replace", index=False)
    conn.close()
    print("Database created successfully.")

if __name__ == "__main__":
    create_database()
