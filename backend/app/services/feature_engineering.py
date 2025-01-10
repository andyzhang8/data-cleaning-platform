import pandas as pd

def combine_columns(df: pd.DataFrame, new_column: str, columns: list, separator: str = " ") -> pd.DataFrame:
    if not all(col in df.columns for col in columns):
        raise ValueError(f"One or more columns {columns} not found in the DataFrame.")
    df[new_column] = df[columns].astype(str).agg(separator.join, axis=1)
    return df

def split_column(df: pd.DataFrame, column: str, new_columns: list, separator: str = " ") -> pd.DataFrame:
    if column not in df.columns:
        raise ValueError(f"Column {column} not found in the DataFrame.")
    split_data = df[column].str.split(separator, expand=True)
    if len(new_columns) > split_data.shape[1]:
        raise ValueError("Number of new columns exceeds the splits available.")
    for i, new_col in enumerate(new_columns):
        df[new_col] = split_data[i]
    return df

def create_derived_column(df: pd.DataFrame, new_column: str, formula: str) -> pd.DataFrame:
    try:
        df[new_column] = eval(formula)
    except Exception as e:
        raise ValueError(f"Error in formula evaluation: {e}")
    return df
