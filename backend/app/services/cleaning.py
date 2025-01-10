import pandas as pd
from app.services.feature_engineering import combine_columns, split_column, create_derived_column

def drop_columns(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    return df.drop(columns=columns, errors="ignore")

def rename_columns(df: pd.DataFrame, columns: dict) -> pd.DataFrame:
    return df.rename(columns=columns)

def fill_missing_values(df: pd.DataFrame, strategy: str = "mean") -> pd.DataFrame:
    if strategy == "mean":
        return df.fillna(df.mean())
    elif strategy == "median":
        return df.fillna(df.median())
    elif strategy == "zero":
        return df.fillna(0)
    else:
        raise ValueError(f"Unknown fill strategy: {strategy}")

def drop_missing_data(df: pd.DataFrame) -> pd.DataFrame:
    return df.dropna()

def change_data_types(df: pd.DataFrame, column_types: dict) -> pd.DataFrame:
    for col, dtype in column_types.items():
        if col in df:
            df[col] = df[col].astype(dtype)
    return df

def normalize_columns(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    for col in columns:
        if col in df:
            df[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min())
    return df

def standardize_columns(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    from scipy.stats import zscore
    for col in columns:
        if col in df:
            df[col] = zscore(df[col])
    return df

def log_transform(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    for col in columns:
        if col in df and (df[col] > 0).all():  # Ensure no negative or zero values
            df[col] = df[col].apply(lambda x: np.log(x))
    return df

def detect_outliers(df: pd.DataFrame, columns: list, method: str = "z-score") -> pd.DataFrame:
    if method == "z-score":
        from scipy.stats import zscore
        for col in columns:
            if col in df:
                df = df[df[col].apply(lambda x: abs(zscore([x]))[0] < 3)]
    elif method == "iqr":
        for col in columns:
            if col in df:
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                df = df[(df[col] >= Q1 - 1.5 * IQR) & (df[col] <= Q3 + 1.5 * IQR)]
    else:
        raise ValueError(f"Unknown outlier detection method: {method}")
    return df

def extract_date_components(df: pd.DataFrame, column: str, components: list) -> pd.DataFrame:
    if column not in df.columns:
        raise ValueError(f"Column {column} not found in the DataFrame.")
    if not pd.api.types.is_datetime64_any_dtype(df[column]):
        df[column] = pd.to_datetime(df[column])

    for component in components:
        if component == "year":
            df[f"{column}_year"] = df[column].dt.year
        elif component == "month":
            df[f"{column}_month"] = df[column].dt.month
        elif component == "day":
            df[f"{column}_day"] = df[column].dt.day
        else:
            raise ValueError(f"Unknown component: {component}")
    return df

def advanced_transformations(
    df: pd.DataFrame, operations: dict
) -> pd.DataFrame:

    if "combine_columns" in operations:
        df = combine_columns(
            df,
            operations["combine_columns"]["new_column"],
            operations["combine_columns"]["columns"],
            operations["combine_columns"].get("separator", " "),
        )

    if "split_column" in operations:
        df = split_column(
            df,
            operations["split_column"]["column"],
            operations["split_column"]["new_columns"],
            operations["split_column"].get("separator", " "),
        )

    if "create_derived_column" in operations:
        df = create_derived_column(
            df,
            operations["create_derived_column"]["new_column"],
            operations["create_derived_column"]["formula"],
        )

    return df