import pandas as pd
import numpy as np

def transform_data(df):
    # Buang data dengan Title "Unknown Product"
    df = df[df['Title'] != 'Unknown Product'].copy()

    def clean_price(p):
        try:
            val = float(p.replace('$', '').strip())
            return val if val > 0 else np.nan
        except:
            return np.nan

    df['Price'] = df['Price'].apply(clean_price)
    df['Price'] = df['Price'] * 16000

    def clean_rating(r):
        try:
            r_str = str(r).replace("Not Rated", "").strip()
            return float(r_str)
        except:
            return np.nan

    df['Rating'] = df['Rating'].apply(clean_rating)
    df['Colors'] = pd.to_numeric(df['Colors'], errors='coerce')
    df['Size'] = df['Size'].astype(str).str.strip()
    df['Gender'] = df['Gender'].astype(str).str.strip()

    df = df.dropna()
    df = df.drop_duplicates()
    df = df.reset_index(drop=True)

    df['Colors'] = df['Colors'].astype(int)

    return df
