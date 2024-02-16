import os
import pytest


@pytest.fixture(scope="session")
def data_directory():
    # Get the absolute path of the directory containing the data files
    tests_directory = os.path.dirname(os.path.abspath(__file__))
    project_directory = os.path.join(tests_directory, "..")
    data_directory = os.path.join(project_directory, "abis")

    return data_directory
