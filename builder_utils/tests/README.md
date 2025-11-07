# Skill Building Helpers - Test Suite

This directory contains a comprehensive test suite for all skill building helper tools and frameworks.

## Test Organization

### Core Test Files

- **`test_packages_and_connections.py`** - Tests all package imports from pyproject.toml and AnswerRocket client connections
- **`test_helper_utilities.py`** - Tests the functionality of helper tools (py_ex.py, viz_previewer.py, etc.)
- **`test_visualization_framework.py`** - Tests visualization creation, validation, and preview functionality

### Example/Integration Tests

- **`test_skill_preview_example.py`** - Example skill demonstrating preview functionality
- **`test_executor_integration.py`** - Integration tests for the executor with visualization testing

### Test Runner

- **`run_all_tests.py`** - Main test runner that can execute all tests or individual test files

## Usage

### Run All Tests
```bash
# From the project root
python skill-building-helpers/tests/run_all_tests.py

# Or from the tests directory
cd skill-building-helpers/tests
python run_all_tests.py
```

### Run Individual Test Files
```bash
# Run specific test file
python skill-building-helpers/tests/run_all_tests.py test_packages_and_connections.py

# Or run directly
python skill-building-helpers/tests/test_packages_and_connections.py
```

### List Available Tests
```bash
python skill-building-helpers/tests/run_all_tests.py --list
```

### Verbose Output
```bash
python skill-building-helpers/tests/run_all_tests.py --verbose
```

## Test Categories

### 1. Package and Connection Tests (`test_packages_and_connections.py`)
- ✅ NumPy import and functionality
- ✅ Pandas import and functionality  
- ✅ Playwright import and functionality
- ✅ Pytest import and functionality
- ✅ Python-dotenv import and functionality
- ✅ Skill Framework import and functionality
- ✅ AnswerRocket Client import and functionality
- ✅ AnswerRocket API connection testing
- ✅ Environment variable validation
- ✅ SQL query execution testing

### 2. Helper Utilities Tests (`test_helper_utilities.py`)
- ✅ FileExecutor (py_ex.py) functionality
- ✅ VisualizationTester import validation
- ✅ Skill framework preview functionality
- ✅ JSON validation
- ✅ File structure validation

### 3. Visualization Framework Tests (`test_visualization_framework.py`)
- ✅ SkillVisualization creation
- ✅ Highcharts visualization setup
- ✅ ExportData creation
- ✅ SkillOutput creation
- ✅ JSON layout validation
- ✅ Preview skill function testing

### 4. Integration Tests
- ✅ Executor integration with visualization testing
- ✅ End-to-end skill preview examples

## Environment Requirements

The tests require:
- Python 3.11+
- All packages from `pyproject.toml` installed
- Environment variables configured (for connection tests):
  - `AR_URL`
  - `AR_TOKEN`
  - `DATASET_ID`
  - `DATABASE_ID`

## Test Output

Each test provides:
- ✅ Success indicators for passed tests
- ❌ Failure indicators with error details
- 📊 Summary statistics
- 🎉 Overall success confirmation

## Adding New Tests

To add new tests:

1. Create a new test file following the naming pattern `test_*.py`
2. Include a `main()` function that returns 0 for success, 1 for failure
3. Add appropriate imports and path setup for helper modules
4. Follow the existing test structure and output formatting
5. The test runner will automatically discover and include new test files

## Integration with py_ex.py

All test files can be executed using the `py_ex.py` executor:

```bash
python skill-building-helpers/py_ex.py skill-building-helpers/tests/test_packages_and_connections.py
```

This provides consistent execution environment and output formatting across all tests.
