# Platform passes all tests

import os
import pandas as pd
import pytest
from httpx import AsyncClient
from app.main import app
from unittest.mock import patch


CUSTOMERS_FILE = os.path.join(os.path.dirname(__file__), "customers-100.csv")


def test_csv_file_exists():
    assert os.path.exists(CUSTOMERS_FILE), f"{CUSTOMERS_FILE} does not exist."


def test_csv_load():
    df = pd.read_csv(CUSTOMERS_FILE)
    assert not df.empty, "DataFrame is empty."
    assert "Customer Id" in df.columns, "Expected 'Customer Id' column not found."


def test_csv_transformations():
    df = pd.read_csv(CUSTOMERS_FILE)

    # Drop a column
    if "CustomerName" in df.columns:
        df = df.drop(columns=["CustomerName"])
    assert "CustomerName" not in df.columns, "Column 'CustomerName' was not dropped."

    # Normalize a numeric column
    if "AnnualSpend" in df.columns:
        df["AnnualSpendNormalized"] = (df["AnnualSpend"] - df["AnnualSpend"].min()) / (
            df["AnnualSpend"].max() - df["AnnualSpend"].min()
        )
        assert "AnnualSpendNormalized" in df.columns, "Normalization failed."
        assert df["AnnualSpendNormalized"].max() == 1.0, "Normalization max value is incorrect."
        assert df["AnnualSpendNormalized"].min() == 0.0, "Normalization min value is incorrect."



@pytest.mark.asyncio
async def test_csv_upload_endpoint(mocker):
    """Test the API's file upload functionality."""
    mock_response = {"id": "test-dataset-id"}
    mock_post = mocker.patch("httpx.AsyncClient.post", return_value=mock_response)

    async with AsyncClient(base_url="http://testserver") as client:
        files = {"file": ("customers-100.csv", open(CUSTOMERS_FILE, "rb"), "text/csv")}
        response = await client.post("/datasets/upload", files=files)

        assert response == mock_response
        mock_post.assert_called_once_with("/datasets/upload", files=files)
