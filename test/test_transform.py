import pandas as pd
import pytest
import numpy as np
from utils.transform import transform_data


def test_transform_valid_data():
    df = pd.DataFrame({
        'Title': ['Product A', 'Product B'],
        'Price': ['$10', '$20'],
        'Rating': ['4.5', '5.0'],
        'Colors': ['3', '5'],
        'Size': ['M', 'L'],
        'Gender': ['Male', 'Female'],
        'Timestamp': ['2024-05-17T10:00:00', '2024-05-17T10:00:00']
    })
    result = transform_data(df)
    assert len(result) == 2
    assert result['Price'].iloc[0] == 160000.0
    assert result['Rating'].iloc[1] == 5.0
    assert result['Colors'].iloc[1] == 5


def test_transform_invalid_price():
    df = pd.DataFrame({
        'Title': ['Product A'],
        'Price': ['???'],
        'Rating': ['4.5'],
        'Colors': ['3'],
        'Size': ['M'],
        'Gender': ['Male'],
        'Timestamp': ['2024-05-17T10:00:00']
    })
    result = transform_data(df)
    assert result.empty


def test_transform_invalid_rating():
    df = pd.DataFrame({
        'Title': ['Product A'],
        'Price': ['$10'],
        'Rating': ['Invalid'],
        'Colors': ['3'],
        'Size': ['M'],
        'Gender': ['Male'],
        'Timestamp': ['2024-05-17T10:00:00']
    })
    result = transform_data(df)
    assert result.empty
