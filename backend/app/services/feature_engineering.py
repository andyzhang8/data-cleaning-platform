import pandas as pd

def combine_columns(df: pd.DataFrame, new_column: str, columns: list, separator: str = " ") -> pd.DataFrame:
    """
    Combine specified columns into a new column with a separator.
    """
    if not all(col in df.columns for col in columns):
        raise ValueError(f"One or more columns {columns} not found in the DataFrame.")
    df[new_column] = df[columns].astype(str).agg(separator.join, axis=1)
    return df

def split_column(df: pd.DataFrame, column: str, new_columns: list, separator: str = " ") -> pd.DataFrame:
    """
    Split a column into multiple new columns based on a separator.
    """
    if column not in df.columns:
        raise ValueError(f"Column {column} not found in the DataFrame.")
    split_data = df[column].str.split(separator, expand=True)
    if len(new_columns) > split_data.shape[1]:
        raise ValueError("Number of new columns exceeds the splits available.")
    for i, new_col in enumerate(new_columns):
        df[new_col] = split_data[i]
    return df

def create_derived_column(df: pd.DataFrame, new_column: str, formula: str) -> pd.DataFrame:
    """
    Create a derived column based on a user-defined formula.
    Formula should be a valid Python expression involving column names.
    Example: 'df["col1"] + df["col2"]'
    """
    try:
        df[new_column] = eval(formula)
    except Exception as e:
        raise ValueError(f"Error in formula evaluation: {e}")
    return df
