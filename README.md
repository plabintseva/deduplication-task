# deduplication-task

In general, to address this task, I would use existing pandas method `duplicated`, since it's already well optimized. 

As an example, the function could look like this:


```
def check_duplicates(df: pd.DataFrame, columns: list) -> dict:
    is_valid_input(df, columns)

    duplicates = df.duplicated(subset=columns, keep=False)

    count = duplicates.sum()
    if count > 0:
        samples = df[duplicates].groupby(columns).size().reset_index(name='number_of_duplicates')
    else:
        samples = pd.DataFrame(columns=[*columns, 'number_of_duplicates'])
    return {'count': count, 'samples': samples}
```
But I also implemented a custom version, which uses `groupby`. The implementation could be found under `src` folder.

## How to test (Unix/macOS)

### Setting Up a Virtual Environment 
Creating a virtual environment allows you to manage project-specific dependencies separately from your global Python setup. Here's how to create and activate a virtual environment for this project.

**Navigate to your project directory**:
`cd path/to/deduplication-task`

**Create the virtual environment:**
Replace env_name with the name you want for your virtual environment.
`python3 -m venv env_name`

**Activating the Virtual Environment**
Activate your virtual environment to isolate your project's dependencies.
`source env_name/bin/activate`

**Deactivating the Virtual Environment**
When finished working within the virtual environment, you can deactivate it by running:
`deactivate`

### Installing Project Requirements
After activating the virtual environment, install the project's dependencies listed in the `requirements.txt` file.
Ensure you have a requirements.txt file at the project root with all necessary packages.
Install the requirements using pip:
`pip install -r requirements.txt`

### Running All Tests
Navigate to your project directory where your tests are located.
Run `pytest` without any arguments to execute all test files: `pytest`

### Run a specific test within a file: 
Specify the file name followed by `::` and the test function name:
`pytest path/to/test_file.py::test_function_name`

Specific example:
`pytest tests/deduplicate_test.py::test_with_empty_dataframe`






