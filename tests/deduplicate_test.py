import numpy as np
import pandas as pd
import pytest

from src.deduplicate import check_duplicates_custom
from src.helpers import InputValidationError


def test_with_incorrect_format_of_first_argument():
    """
      Verify `check_duplicates_custom` raises `InputValidationError` if the first argument is not a DataFrame.

      A list is passed as the first argument to trigger the validation error, expecting a specific error message.

      Raises:
          AssertionError: If the expected exception is not raised or the error message doesn't match.
    """
    df_list = ['blabla', 'bla']
    with pytest.raises(InputValidationError) as e:
        check_duplicates_custom(df_list, ['col_1'])
    assert str(e.value) == "The first argument must be a pd.DataFrame."


def test_with_non_existing_column():
    """
    Check `check_duplicates_custom` raises `InputValidationError` for a non-existent column in the DataFrame.

    The function is tested with a column name ('col_5') not present in the DataFrame, expecting an error message
    that the specified column does not exist.

    Raises:
        AssertionError: If no exception is raised or the error message is incorrect.
    """
    df_1 = pd.DataFrame(
        data=[
            ['A', 'a', 'x', 1],
            ['A', 'b', 'x', 1],
            ['A', 'c', 'x', 1],
            ['B', 'a', 'x', 1],
            ['B', 'b', 'x', 1],
            ['B', 'c', 'x', 1],
            ['A', 'a', 'y', 1],
        ],
        columns=['col_1', 'col_2', 'col_3', 'col_4']
    )
    with pytest.raises(InputValidationError) as e:
        check_duplicates_custom(df_1, ['col_1', 'col_5'])
    assert str(e.value) == "Column ['col_5'] does not exist in the dataframe."


def test_with_incorrect_format_of_second_argument():
    """
    Tests that `check_duplicates_custom` raises `InputValidationError` when the second argument is not a list.

    A non-list type (integer) is passed as the second argument to prompt the expected validation error.

    Raises:
        AssertionError: If the expected exception is not raised or the message differs from the expected.
    """
    df_1 = pd.DataFrame(
        data=[
            ['A', 'a', 'x', 1],
            ['A', 'b', 'x', 1],
            ['A', 'c', 'x', 1],
            ['B', 'a', 'x', 1],
            ['B', 'b', 'x', 1],
            ['B', 'c', 'x', 1],
            ['A', 'a', 'y', 1],
        ],
        columns=['col_1', 'col_2', 'col_3', 'col_4']
    )
    with pytest.raises(InputValidationError) as e:
        check_duplicates_custom(df_1, 3)
    assert str(e.value) == "The second argument must be a list of column names."


def test_with_empty_dataframe():
    """
    Verifies `check_duplicates_custom` raises `InputValidationError` for an empty DataFrame.

    Tests the function's response to an empty DataFrame and an empty list of columns,
    expecting an error message that the DataFrame should not be empty.

    Raises:
        AssertionError: If the expected exception and message are not raised.
    """
    df_empty = pd.DataFrame()
    with pytest.raises(InputValidationError) as e:
        _ = check_duplicates_custom(df_empty, [])
    assert str(e.value) == "DataFrame should not be empty."


def test_with_empty_columns_list():
    """
    Checks `check_duplicates_custom` raises `InputValidationError` when columns list is empty.

    Ensures the function flags an error for not specifying columns to check for duplicates in a populated DataFrame.

    Raises:
        AssertionError: If the function doesn't raise the expected exception or the error message differs.
    """
    df_1 = pd.DataFrame(
        data=[
            ['A', 'a', 'x', 1],
            ['A', 'b', 'x', 1],
            ['A', 'c', 'x', 1],
            ['B', 'a', 'x', 1],
            ['B', 'b', 'x', 1],
            ['B', 'c', 'x', 1],
            ['A', 'a', 'y', 1],
        ],
        columns=['col_1', 'col_2', 'col_3', 'col_4']
    )
    with pytest.raises(InputValidationError) as e:
        _ = check_duplicates_custom(df_1, [])
    assert str(e.value) == "Columns list should not be empty."


def test_with_correct_setup():
    """
    Verifies `check_duplicates_custom` accurately identifies and counts duplicates under various conditions.

    This test checks for duplicates:
    1. In a single column.
    2. Across multiple columns.
    3. Across columns, where no duplicates are expected.

    It asserts the correct duplicate counts and compares the resulting samples DataFrame against expected outcomes
    for scenarios 1 and 2, and checks for no duplicates in scenario 3.
    """
    df_1 = pd.DataFrame(
        data=[
            ['A', 'a', 'x', 1],
            ['A', 'b', 'x', 1],
            ['A', 'c', 'x', 1],
            ['B', 'a', 'x', 1],
            ['B', 'b', 'x', 1],
            ['B', 'c', 'x', 1],
            ['A', 'a', 'y', 1],
        ],
        columns=['col_1', 'col_2', 'col_3', 'col_4']
    )
    result_1 = check_duplicates_custom(df_1, ['col_1'])
    result_2 = check_duplicates_custom(df_1, ['col_1', 'col_2'])
    result_3 = check_duplicates_custom(df_1, ['col_1', 'col_2', 'col_3'])

    expected_samples_1 = pd.DataFrame(
        data=[
            ['A', 4],
            ['B', 3],
        ],
        columns=['col_1', 'number_of_duplicates']
    )

    expected_samples_2 = pd.DataFrame(
        data=[
            ['A', 'a', 2],
        ],
        columns=['col_1', 'col_2', 'number_of_duplicates']
    )

    assert result_1['count'] == 7
    pd.testing.assert_frame_equal(result_1['samples'], expected_samples_1)
    assert result_2['count'] == 2
    pd.testing.assert_frame_equal(result_2['samples'], expected_samples_2)
    assert result_3['count'] == 0
    assert result_3['samples'].empty


def test_with_all_unique_rows():
    """
    Validates that `check_duplicates_custom` correctly identifies a DataFrame with all unique rows,
    resulting in no duplicates found.

    A DataFrame is constructed with entirely unique rows across specified columns, and the function
    is expected to return a count of 0 for duplicates and an empty DataFrame for samples.
    """
    df = pd.DataFrame(
        data=[
            ['A', 1, 'W'],
            ['B', 2, 'X'],
            ['C', 3, 'Y'],
            ['D', 4, 'Z']
        ],
        columns=['col_1', 'col_2', 'col_3']
    )
    columns = ['col_1', 'col_2', 'col_3']
    result = check_duplicates_custom(df, columns)
    assert result['count'] == 0
    assert result['samples'].empty


def test_with_missing_values():
    """
    Tests `check_duplicates_custom` for its handling of missing values (NaNs) in a DataFrame.

    Constructs a DataFrame with both complete and incomplete (NaN-containing) rows to check
    how duplicates are identified in presence of NaNs. Assumes rows with NaNs in the specified
    columns are not treated as duplicates of each other.

    The test verifies that only complete rows with identical values are counted as duplicates,
    expecting a specific count of duplicates and a non-empty samples DataFrame.
    """
    df = pd.DataFrame(
        data=[
            ['A', 1, 'X'],
            ['A', 1, 'X'],
            [np.nan, np.nan, 'Y'],
            [np.nan, np.nan, 'W'],
            ['B', 2, np.nan]
        ],
        columns=['col_1', 'col_2', 'col_3']
    )
    columns = ['col_1', 'col_2']
    result = check_duplicates_custom(df, columns)
    # This example assumes rows with NaNs are not considered duplicates of each other.
    assert result['count'] == 2  # Two duplicates for 'A' and 1
    assert not result['samples'].empty

