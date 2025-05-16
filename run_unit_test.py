""" Unit test runner for the 'tests' directory.
This script discovers and runs all unit tests in the specified directory.
It will test all 16 files matching the pattern 'test_*.py'.
The test results will be displayed in the console, and the script will exit with a status code
indicating success (0) or failure (1).
"""

import unittest

# Discover and run all test cases in the 'tests' directory
if __name__ == "__main__":
    # Create a test loader to discover tests in the 'tests' directory
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir="tests", pattern="test_*.py")

    # Create a test runner to run the test suite
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Exit with a status code based on the test results
    if result.wasSuccessful():
        exit(0)
    else:
        exit(1)