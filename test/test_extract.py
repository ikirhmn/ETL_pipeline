import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.extract import extract_data

def test_extract_returns_dataframe():
    df = extract_data()
    assert isinstance(df, pd.DataFrame), "Hasil extract_data harus berupa DataFrame"

def test_extract_not_empty():
    df = extract_data()
    assert not df.empty, "Hasil extract_data tidak boleh kosong"

def test_extract_expected_columns():
    df = extract_data()
    expected_columns = {'Title', 'Price', 'Rating', 'Colors', 'Size', 'Gender'}
    assert expected_columns.issubset(df.columns), f"Kolom harus mengandung: {expected_columns}"