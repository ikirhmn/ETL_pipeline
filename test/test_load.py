import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
from utils.load import (
    load_to_csv, load_to_gsheet, load_to_postgres,
    get_gsheet_client, get_postgres_engine
)


@pytest.fixture
def dummy_df():
    return pd.DataFrame({
        "Name": ["Item 1", "Item 2"],
        "Price": [1000, 2000]
    })


def test_load_to_csv(tmp_path, dummy_df):
    output_file = tmp_path / "test_output.csv"
    load_to_csv(dummy_df, filename=output_file)
    result_df = pd.read_csv(output_file)
    pd.testing.assert_frame_equal(result_df, dummy_df)


@patch("utils.load.ServiceAccountCredentials")
@patch("utils.load.gspread.authorize")
def test_get_gsheet_client(mock_authorize, mock_creds):
    mock_creds.from_json_keyfile_name.return_value = "mocked_creds"
    mock_authorize.return_value = "mocked_client"

    client = get_gsheet_client("dummy_path.json")
    assert client == "mocked_client"


@patch("utils.load.get_gsheet_client")
@patch("utils.load.set_with_dataframe")
def test_load_to_gsheet_existing_sheet(mock_set_df, mock_get_client, dummy_df):
    mock_sheet = MagicMock()
    mock_sheet.title = "Sheet1"
    mock_spreadsheet = MagicMock()
    mock_spreadsheet.title = "Mocked Spreadsheet"
    mock_spreadsheet.worksheet.return_value = mock_sheet

    mock_client = MagicMock()
    mock_client.open_by_key.return_value = mock_spreadsheet
    mock_get_client.return_value = mock_client

    load_to_gsheet(dummy_df, "spreadsheet_id", "Sheet1", creds_path="dummy.json")

    mock_sheet.clear.assert_called_once()
    mock_set_df.assert_called_once_with(mock_sheet, dummy_df)

from gspread.exceptions import WorksheetNotFound  # ⬅️ tambahin ini di atas

@patch("utils.load.get_gsheet_client")
@patch("utils.load.set_with_dataframe")
def test_load_to_gsheet_missing_sheet_creates_new(mock_set_df, mock_get_client, dummy_df):
    mock_sheet = MagicMock()
    mock_sheet.title = "CreatedSheet"
    mock_spreadsheet = MagicMock()
    mock_spreadsheet.title = "New Spreadsheet"

    # ⬇️ Ini yang diperbaiki
    mock_spreadsheet.worksheet.side_effect = WorksheetNotFound("Sheet not found")
    mock_spreadsheet.add_worksheet.return_value = mock_sheet

    mock_client = MagicMock()
    mock_client.open_by_key.return_value = mock_spreadsheet
    mock_get_client.return_value = mock_client

    load_to_gsheet(dummy_df, "spreadsheet_id", "CreatedSheet", creds_path="dummy.json")

    mock_sheet.clear.assert_called_once()
    mock_set_df.assert_called_once_with(mock_sheet, dummy_df)



@patch("utils.load.create_engine")
def test_get_postgres_engine(mock_create_engine):
    mock_create_engine.return_value = "mocked_engine"
    engine = get_postgres_engine("test_db", "user", "pass")
    assert engine == "mocked_engine"


@patch("utils.load.get_postgres_engine")
def test_load_to_postgres(mock_get_engine, dummy_df):
    mock_engine = MagicMock()
    mock_get_engine.return_value = mock_engine

    with patch.object(dummy_df, "to_sql") as mock_to_sql:
        load_to_postgres(dummy_df, "db", "user", "pw")
        mock_to_sql.assert_called_once_with("products", mock_engine, if_exists='replace', index=False)
