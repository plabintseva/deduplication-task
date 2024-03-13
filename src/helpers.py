import pandas as pd


class InputValidationError(ValueError):
    """Exception raised for errors in the input."""
    pass


def is_valid_input(df: pd.DataFrame, columns: list) -> None:
    """
    Validate input dataframe and columns list.

    Parameters:
    - df (pd.DataFrame): The dataframe to check.
    - columns (list): A list of column names to verify in the dataframe.

    Raises:
    - InputValidationError: If any input validation check fails.
    """
    if not isinstance(df, pd.DataFrame):
        raise InputValidationError("The first argument must be a pd.DataFrame.")

    if df.empty:
        raise InputValidationError("DataFrame should not be empty.")

    if not isinstance(columns, list):
        raise InputValidationError("The second argument must be a list of column names.")

    if not all(isinstance(col, str) for col in columns):
        raise InputValidationError("Columns names should be strings.")

    if isinstance(columns, list) and len(columns) == 0:
        raise InputValidationError("Columns list should not be empty.")

    missing_columns = [col for col in columns if col not in df.columns]
    if missing_columns:
        raise InputValidationError(f"Column {missing_columns} does not exist in the dataframe.")