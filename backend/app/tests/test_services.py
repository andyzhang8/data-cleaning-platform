# Platform passes all tests

import pytest
import pandas as pd
from app.services.cleaning import (
    drop_columns,
    fill_missing_values,
    normalize_columns,
    detect_outliers,
)
from app.services.feature_engineering import (
    combine_columns,
    split_column,
    create_derived_column,
)


def test_drop_columns():
    df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    result = drop_columns(df, ["a"])
    assert "a" not in result.columns


def test_fill_missing_values_mean():
    df = pd.DataFrame({"a": [1, None, 3]})
    result = fill_missing_values(df, "mean")
    assert result["a"].isnull().sum() == 0
    assert result["a"].iloc[1] == 2 


def test_normalize_columns():
    df = pd.DataFrame({"a": [1, 2, 3]})
    result = normalize_columns(df, ["a"])
    assert result["a"].min() == 0
    assert result["a"].max() == 1


def test_detect_outliers_zscore():
    df = pd.DataFrame({"a": [1, 2, 100]})
    result = detect_outliers(df, ["a"], method="z-score")
    assert len(result) < len(df)


def test_combine_columns():
    df = pd.DataFrame({"first_name": ["John"], "last_name": ["Doe"]})
    result = combine_columns(df, "full_name", ["first_name", "last_name"], " ")
    assert "full_name" in result.columns
    assert result["full_name"].iloc[0] == "John Doe"


def test_split_column():
    df = pd.DataFrame({"full_name": ["John Doe"]})
    result = split_column(df, "full_name", ["first_name", "last_name"], " ")
    assert "first_name" in result.columns
    assert result["first_name"].iloc[0] == "John"
    assert "last_name" in result.columns
    assert result["last_name"].iloc[0] == "Doe"


def test_create_derived_column():
    df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    result = create_derived_column(df, "sum", "df['a'] + df['b']")
    assert "sum" in result.columns
    assert result["sum"].iloc[0] == 4
    assert result["sum"].iloc[1] == 6
