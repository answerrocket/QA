#!/usr/bin/env python3
"""
Main Test Runner for Skill Building Helpers
Runs all test suites or individual test files
"""

import sys
import os
import argparse
import subprocess
from pathlib import Path
from typing import List, Dict, Tuple

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def run_test_file(test_file: Path, verbose: bool = False) -> Tuple[bool, str, str]:
    """
    Run a single test file and return results
    
    Args:
        test_file: Path to the test file
        verbose: Whether to show detailed output
    
    Returns:
        Tuple of (success, stdout, stderr)
    """
    try:
        result = subprocess.run(
            [sys.executable, str(test_file)],
            capture_output=True,
            text=True,
            cwd=test_file.parent,
            timeout=120  # 2 minute timeout per test file
        )
        
        success = result.returncode == 0
        return success, result.stdout, result.stderr
        
    except subprocess.TimeoutExpired:
        return False, "", "Test timed out after 120 seconds"
    except Exception as e:
        return False, "", f"Error running test: {str(e)}"

def discover_test_files() -> List[Path]:
    """Discover all test files in the tests directory"""
    test_dir = Path(__file__).parent
    test_files = []
    
    # Find all Python files that start with 'test_'
    for file_path in test_dir.glob("test_*.py"):
        if file_path.name != "run_all_tests.py":  # Exclude this runner
            test_files.append(file_path)
    
    return sorted(test_files)

def print_test_summary(results: Dict[str, Tuple[bool, str, str]], verbose: bool = False):
    """Print a summary of all test results"""
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    total_tests = len(results)
    passed_tests = sum(1 for success, _, _ in results.values() if success)
    failed_tests = total_tests - passed_tests
    
    print(f"Total test files: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {failed_tests}")
    print()
    
    # Show individual results
    for test_name, (success, stdout, stderr) in results.items():
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{status}: {test_name}")
        
        if verbose or not success:
            if stdout:
                print(f"  STDOUT:\n{stdout}")
            if stderr:
                print(f"  STDERR:\n{stderr}")
            print()
    
    if passed_tests == total_tests:
        print("🎉 ALL TESTS PASSED!")
    else:
        print(f"⚠️ {failed_tests} TEST(S) FAILED")

def main():
    """Main test runner function"""
    parser = argparse.ArgumentParser(description="Run skill building helper tests")
    parser.add_argument(
        "test_file", 
        nargs="?", 
        help="Specific test file to run (optional)"
    )
    parser.add_argument(
        "-v", "--verbose", 
        action="store_true", 
        help="Show verbose output"
    )
    parser.add_argument(
        "-l", "--list", 
        action="store_true", 
        help="List available test files"
    )
    
    args = parser.parse_args()
    
    # Discover test files
    test_files = discover_test_files()
    
    if args.list:
        print("Available test files:")
        for test_file in test_files:
            print(f"  - {test_file.name}")
        return 0
    
    if args.test_file:
        # Run specific test file
        test_path = Path(__file__).parent / args.test_file
        if not test_path.exists():
            print(f"❌ Test file not found: {args.test_file}")
            return 1
        
        print(f"Running single test: {args.test_file}")
        print("="*50)
        
        success, stdout, stderr = run_test_file(test_path, args.verbose)
        
        print(stdout)
        if stderr:
            print("STDERR:")
            print(stderr)
        
        if success:
            print("✅ TEST PASSED")
            return 0
        else:
            print("❌ TEST FAILED")
            return 1
    
    else:
        # Run all tests
        print("SKILL BUILDING HELPERS - COMPREHENSIVE TEST SUITE")
        print("="*80)
        print(f"Python version: {sys.version}")
        print(f"Test directory: {Path(__file__).parent}")
        print(f"Found {len(test_files)} test files")
        print()
        
        results = {}
        
        for test_file in test_files:
            test_name = test_file.name
            print(f"Running {test_name}...")
            
            success, stdout, stderr = run_test_file(test_file, args.verbose)
            results[test_name] = (success, stdout, stderr)
            
            if success:
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
                if not args.verbose and stderr:
                    print(f"  Error: {stderr.strip()}")
            
            if args.verbose:
                if stdout:
                    print(f"  Output:\n{stdout}")
                if stderr:
                    print(f"  Errors:\n{stderr}")
            
            print()
        
        # Print summary
        print_test_summary(results, args.verbose)
        
        # Return appropriate exit code
        failed_count = sum(1 for success, _, _ in results.values() if not success)
        return 1 if failed_count > 0 else 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
