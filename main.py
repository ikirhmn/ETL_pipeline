from utils.extract import extract_data
from utils.transform import transform_data
from utils.load import load_to_csv, load_to_gsheet, load_to_postgres

import os

def main():
    print("[1] Starting ETL pipeline...")

    # Step 1: Extract
    print("[2] Extracting data...")
    raw_df = extract_data()
    if raw_df.empty:
        print("[X] Data extraction failed or returned empty DataFrame.")
        return
    print(f"[✓] Extracted {len(raw_df)} rows.")

    # Step 2: Transform
    print("[3] Transforming data...")
    clean_df = transform_data(raw_df)
    print(f"[✓] Transformed to {len(clean_df)} clean rows.")

    # Step 3a: Load to CSV
    print("[4] Loading to CSV...")
    load_to_csv(clean_df, filename="product.csv")

    # Step 3b: Load to Google Sheets
    spreadsheet_id = os.getenv("GSHEET_ID", "1uVHGPZVP8YTV7o6msLMliSqWz3_DhswVrWxqiTovRc0")
    sheet_name = os.getenv("GSHEET_SHEET", "ETL_pipeline")
    creds_path = os.getenv("GSHEET_CREDENTIALS", "google-sheets-api.json")
    
    print("[5] Loading to Google Sheets...")
    load_to_gsheet(clean_df, spreadsheet_id, sheet_name, creds_path=creds_path)

    # Step 3c: Load to PostgreSQL
    print("[6] Loading to PostgreSQL...")
    db_name = os.getenv("PG_DB", "etl_pipeline")
    user = os.getenv("PG_USER", "postgres")
    password = os.getenv("PG_PASSWORD", "postgres")
    host = os.getenv("PG_HOST", "localhost")
    port = int(os.getenv("PG_PORT", 5432))

    load_to_postgres(clean_df, db_name, user, password, host=host, port=port)

    print("[✓] ETL pipeline complete 🚀")

if __name__ == "__main__":
    main()
