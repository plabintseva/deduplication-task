import pandas as pd

from src.helpers import is_valid_input


def check_duplicates_custom(df: pd.DataFrame, columns: list) -> dict:
    """
    Identifies and counts duplicate rows in a DataFrame based on specified columns.

    This function first validates the input DataFrame and columns list.
    It then groups the DataFrame by the specified columns and counts the occurrences of each unique group,
    identifying duplicates as any group with more than one occurrence.

    Parameters:
        df (pd.DataFrame): The DataFrame to check for duplicates.
        columns (list): A list of column names to use for identifying duplicates.

    Returns:
        dict: A dictionary containing:
            - 'count': The total number of duplicate occurrences.
            - 'samples': A DataFrame with details of the duplicates, including the count of each duplicate group.

    Note:
        The function counts all occurrences of duplicates by default.
        To exclude the first occurrence from the count, uncomment the relevant line.
    """
    is_valid_input(df, columns)

    grouped_df = df.groupby(columns).size().reset_index(name='number_of_duplicates')
    duplicates = grouped_df[grouped_df['number_of_duplicates'] > 1]

    count = duplicates['number_of_duplicates'].sum()
    # if we don't want to count first occurrence next line should be used
    # count = duplicates['number_of_duplicates'].sum() - duplicates.shape[0]

    return {'count': count, 'samples': duplicates}
