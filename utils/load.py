import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe
from oauth2client.service_account import ServiceAccountCredentials
from sqlalchemy import create_engine

def load_to_csv(df, filename="output.csv"):
    try:
        df.to_csv(filename, index=False)
        print(f"[✓] Data berhasil disimpan ke CSV: {filename}")
    except Exception as e:
        print(f"[X] Gagal simpan ke CSV: {e}")

def get_gsheet_client(creds_path):
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
    return gspread.authorize(creds)

def load_to_gsheet(df, spreadsheet_id, sheet_name, creds_path="google-sheets-api.json"):
    try:
        client = get_gsheet_client(creds_path)
        spreadsheet = client.open_by_key(spreadsheet_id)

        try:
            sheet = spreadsheet.worksheet(sheet_name)
        except gspread.WorksheetNotFound:
            sheet = spreadsheet.add_worksheet(title=sheet_name, rows="1000", cols="20")

        sheet.clear()
        set_with_dataframe(sheet, df)

        print(f"[✓] Data berhasil disimpan ke Google Sheets: {spreadsheet.title} / Sheet: {sheet.title}")
    except Exception as e:
        print(f"[X] Gagal simpan ke Google Sheets: {e}")

def get_postgres_engine(db_name, user, password, host='localhost', port=5432):
    return create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}')

def load_to_postgres(df, db_name, user, password, host='localhost', port=5432, table_name='products'):
    try:
        engine = get_postgres_engine(db_name, user, password, host, port)
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        print(f"[✓] Data berhasil dimuat ke PostgreSQL table: {table_name}")
    except Exception as e:
        print(f"[X] Gagal simpan ke PostgreSQL: {e}")
