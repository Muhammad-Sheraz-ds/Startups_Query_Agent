import pandas as pd
import os

def handle_columns(df):
    """
    Handles the transformation and validation of each column in the dataset.
    """
    # Define handling logic for each column
    column_transformations = {
        'company_id': lambda x: x.fillna(-1).astype(int),
        'company_name': lambda x: x.fillna('Unknown'),
        'short_description': lambda x: x.fillna('No description available'),
        'long_description': lambda x: x.fillna('No detailed description available'),
        'batch': lambda x: x.fillna('Unknown'),
        'status': lambda x: x.fillna('Unknown'),
        'tags': lambda x: x.fillna('Not tagged'),
        'location': lambda x: x.fillna('Unknown'),
        'country': lambda x: x.fillna('Unknown'),
        'year_founded': lambda x: pd.to_numeric(x, errors='coerce').fillna(-1).astype(int),
        'num_founders': lambda x: x.fillna(0).astype(int),
        'founders_names': lambda x: x.fillna('Not available'),
        'team_size': lambda x: pd.to_numeric(x, errors='coerce').fillna(-1).astype(int),
        'website': lambda x: x.fillna('No website available'),
        'cb_url': lambda x: x.fillna('No Crunchbase URL'),
        'linkedin_url': lambda x: x.fillna('No LinkedIn URL')
    }

    # Apply transformations
    for column, transformation in column_transformations.items():
        if column in df.columns:
            df[column] = transformation(df[column])
        else:
            print(f"Warning: Column '{column}' not found in the dataset.")

    return df

def perform_etl(input_path, output_path):
    """
    Performs ETL (Extract, Transform, Load) on the dataset.

    Args:
        input_path (str): Path to the raw data CSV file.
        output_path (str): Path to save the processed data.
    """
    # Step 1: Extract
    print("Extracting data from raw CSV file...")
    df = pd.read_csv(input_path)

    # Step 2: Transform
    print("Transforming data...")
    df = handle_columns(df)

    # Step 3: Load
    print("Saving processed data...")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Processed data saved to {output_path}")

if __name__ == "__main__":
    # Define paths
    raw_data_path = './YC-Scraper/scraper/ycombinator/scraper/data/raw/scraped_data.csv'
    processed_data_path = './YC-Scraper/scraper/ycombinator/scraper/data/processed/processed_data.csv'

    # Perform ETL
    perform_etl(raw_data_path, processed_data_path)
