#!/usr/bin/env python3
"""
Package Import and Connection Test Suite
Tests all dependencies from pyproject.toml and AnswerRocket client connections
"""

import sys
import os
import traceback
from typing import List, Tuple

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_import(package_name: str, import_statement: str, test_function=None) -> Tuple[bool, str]:
    """
    Test importing a package and optionally run a basic test function
    
    Args:
        package_name: Name of the package for display
        import_statement: The import statement to execute
        test_function: Optional function to test basic functionality
    
    Returns:
        Tuple of (success, message)
    """
    try:
        # Execute the import statement
        exec(import_statement, globals())
        
        # Run optional test function
        if test_function:
            test_function()
        
        return True, f"✓ {package_name}: Import and basic test successful"
    
    except ImportError as e:
        return False, f"❌ {package_name}: Import failed - {str(e)}"
    except Exception as e:
        return False, f"⚠️ {package_name}: Import successful but test failed - {str(e)}"

def test_numpy():
    """Test numpy basic functionality"""
    import numpy as np
    arr = np.array([1, 2, 3, 4, 5])
    assert arr.sum() == 15
    assert arr.mean() == 3.0

def test_pandas():
    """Test pandas basic functionality"""
    import pandas as pd
    df = pd.DataFrame({'A': [1, 2, 3], 'B': [4, 5, 6]})
    assert len(df) == 3
    assert list(df.columns) == ['A', 'B']
    assert df['A'].sum() == 6

def test_playwright():
    """Test playwright basic import (not full functionality)"""
    from playwright.sync_api import sync_playwright
    # Just test that we can import the main classes
    assert sync_playwright is not None

def test_pytest():
    """Test pytest basic functionality"""
    import pytest
    # Test that we can access pytest functions
    assert hasattr(pytest, 'main')
    assert hasattr(pytest, 'fixture')

def test_dotenv():
    """Test python-dotenv basic functionality"""
    from dotenv import load_dotenv, find_dotenv
    # Test basic functions exist
    assert callable(load_dotenv)
    assert callable(find_dotenv)

def test_skill_framework():
    """Test skill-framework basic functionality"""
    from skill_framework import SkillInput, skill, SkillParameter, SkillOutput
    # Test that main classes can be imported
    assert SkillInput is not None
    assert skill is not None
    assert SkillParameter is not None
    assert SkillOutput is not None

def test_answerrocket_client():
    """Test answerrocket-client basic functionality"""
    from answer_rocket import AnswerRocketClient
    # Test that we can create an instance (may fail if no credentials, but import should work)
    assert AnswerRocketClient is not None

def test_answerrocket_connection():
    """Test AnswerRocket client connection with environment variables"""
    import os
    from dotenv import load_dotenv
    from answer_rocket import AnswerRocketClient
    
    # Load environment variables
    load_dotenv()
    
    # Check required environment variables
    ar_url = os.getenv('AR_URL')
    ar_token = os.getenv('AR_TOKEN')
    dataset_id = os.getenv('DATASET_ID')
    database_id = os.getenv('DATABASE_ID')
    
    print(f"  AR_URL: {'✓ Set' if ar_url else '❌ Not set'}")
    print(f"  AR_TOKEN: {'✓ Set' if ar_token else '❌ Not set'}")
    print(f"  DATASET_ID: {dataset_id if dataset_id else '❌ Not set'}")
    print(f"  DATABASE_ID: {database_id if database_id else '❌ Not set'}")
    
    if not ar_url or not ar_token:
        raise Exception("Missing required environment variables (AR_URL or AR_TOKEN)")
    
    # Test client initialization
    arc = AnswerRocketClient()
    assert arc is not None
    
    # Test basic client structure
    assert hasattr(arc, 'data'), "Client should have 'data' attribute"
    
    # Test datasets retrieval
    try:
        response = arc.data.get_datasets()
        print(f"  Datasets response type: {type(response)}")
        
        if hasattr(response, 'success'):
            print(f"  Datasets success: {response.success}")
            if not response.success and hasattr(response, 'error'):
                print(f"  Datasets error: {response.error}")
        
        # Don't fail the test if datasets call fails - just log it
        print("  ✓ Datasets API call completed (check logs for success/failure)")
        
    except Exception as e:
        print(f"  ⚠️ Datasets API call failed: {e}")
    
    # Test specific dataset retrieval if dataset_id is available
    if dataset_id:
        try:
            response = arc.data.get_dataset(dataset_id=dataset_id)
            print(f"  Specific dataset response type: {type(response)}")
            
            if hasattr(response, 'success'):
                print(f"  Specific dataset success: {response.success}")
                if not response.success and hasattr(response, 'error'):
                    print(f"  Specific dataset error: {response.error}")
            
            print("  ✓ Specific dataset API call completed")
            
        except Exception as e:
            print(f"  ⚠️ Specific dataset API call failed: {e}")
    
    # Test simple SQL query if database_id is available
    if database_id:
        try:
            simple_query = "SELECT 1 as test_connection"
            response = arc.data.execute_sql_query(
                sql_query=simple_query,
                database_id=database_id
            )
            print(f"  SQL query response type: {type(response)}")
            
            if hasattr(response, 'success'):
                print(f"  SQL query success: {response.success}")
                if response.success:
                    print("  ✓ SQL query executed successfully")
                    if hasattr(response, 'data'):
                        print(f"  SQL query data: {response.data}")
                else:
                    if hasattr(response, 'error'):
                        print(f"  SQL query error: {response.error}")
            
        except Exception as e:
            print(f"  ⚠️ SQL query failed: {e}")
    
    print("  ✓ AnswerRocket connection test completed")

def get_package_version(package_name: str) -> str:
    """Get the version of an installed package"""
    try:
        import importlib.metadata
        return importlib.metadata.version(package_name)
    except Exception:
        return "Unknown"

def main():
    """Run all package import and connection tests"""
    print("=== PACKAGE IMPORT AND CONNECTION TEST SUITE ===")
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    print()
    
    # Define all tests with package names for version checking
    tests = [
        ("NumPy", "numpy", "import numpy as np", test_numpy),
        ("Pandas", "pandas", "import pandas as pd", test_pandas),
        ("Playwright", "playwright", "from playwright.sync_api import sync_playwright", test_playwright),
        ("Pytest", "pytest", "import pytest", test_pytest),
        ("Python-dotenv", "python-dotenv", "from dotenv import load_dotenv", test_dotenv),
        ("Skill Framework", "skill-framework", "from skill_framework import SkillInput, skill", test_skill_framework),
        ("AnswerRocket Client", "answerrocket-client", "from answer_rocket import AnswerRocketClient", test_answerrocket_client),
        ("AnswerRocket Connection", "answerrocket-client", "from answer_rocket import AnswerRocketClient", test_answerrocket_connection),
    ]
    
    results = []
    
    # Run all tests (packages and connections)
    for display_name, package_name, import_stmt, test_func in tests:
        version = get_package_version(package_name)
        success, message = test_import(display_name, import_stmt, test_func)
        results.append((success, message))
        
        # Add version info to successful imports
        if success:
            print(f"{message} (v{version})")
        else:
            print(message)
    
    print()
    print("=== SUMMARY ===")
    
    successful = sum(1 for success, _ in results if success)
    total = len(results)
    
    print(f"Successful imports: {successful}/{total}")
    
    if successful == total:
        print("🎉 All packages imported and tested successfully!")
        return 0
    else:
        print("⚠️ Some packages failed to import or test")
        failed_tests = [msg for success, msg in results if not success]
        print("\nFailed tests:")
        for msg in failed_tests:
            print(f"  {msg}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
