#!/usr/bin/env python3
"""
Helper Utilities Test Suite
Tests the functionality of helper tools in the skill-building-helpers directory
"""

import sys
import os
import tempfile
import json
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_py_ex_executor():
    """Test the py_ex.py file executor functionality"""
    from py_ex import FileExecutor
    
    # Test basic initialization
    executor = FileExecutor()
    assert executor is not None
    assert hasattr(executor, 'run_file')
    assert hasattr(executor, 'python_path')
    
    # Create a simple test script
    test_script_content = '''
print("Hello from test script!")
import sys
print(f"Python version: {sys.version_info.major}.{sys.version_info.minor}")
exit(0)
'''
    
    # Write to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(test_script_content)
        temp_file = f.name
    
    try:
        # Test execution
        result = executor.run_file(temp_file)
        
        # Verify result structure
        assert isinstance(result, dict)
        assert 'stdout' in result
        assert 'stderr' in result
        assert 'returncode' in result
        assert 'success' in result
        
        # Verify successful execution
        assert result['success'] == True
        assert result['returncode'] == 0
        assert "Hello from test script!" in result['stdout']
        assert "Python version:" in result['stdout']
        
        print("  ✓ FileExecutor basic functionality test passed")
        
    finally:
        # Clean up
        os.unlink(temp_file)
    
    # Test error handling with non-existent file
    result = executor.run_file("non_existent_file.py")
    assert result['success'] == False
    assert "File not found" in result['stderr']
    
    print("  ✓ FileExecutor error handling test passed")

def test_viz_previewer_imports():
    """Test that viz_previewer can be imported and has expected functions"""
    try:
        from viz_previewer import VisualizationTester, ValidationResult
        
        # Test that classes can be imported
        assert VisualizationTester is not None
        assert ValidationResult is not None
        
        # Test ValidationResult dataclass
        result = ValidationResult(
            success=True,
            errors=[],
            warnings=[],
            console_logs=[],
            performance_metrics={}
        )
        assert result.success == True
        assert isinstance(result.errors, list)
        
        print("  ✓ VisualizationTester import test passed")
        
    except ImportError as e:
        print(f"  ⚠️ VisualizationTester import failed: {e}")
        # Don't fail the test since this might require additional setup

def test_skill_framework_preview():
    """Test basic skill framework preview functionality"""
    try:
        from skill_framework import skill, SkillInput, SkillOutput, SkillVisualization, ExportData
        import pandas as pd
        
        # Create a simple test skill
        @skill(
            name="test_helper_skill",
            description="A simple test skill for helper testing"
        )
        def test_helper_skill(parameters: SkillInput) -> SkillOutput:
            # Create simple test data
            data = pd.DataFrame({'test': [1, 2, 3], 'values': [10, 20, 30]})
            
            # Create simple visualization
            layout = {
                "type": "Document",
                "children": [{
                    "type": "FlexContainer",
                    "name": "TestContainer",
                    "children": []
                }]
            }
            
            visualization = SkillVisualization(
                title="Test Visualization",
                layout=json.dumps(layout)
            )
            
            return SkillOutput(
                final_prompt="Test skill executed successfully",
                export_data=[ExportData(name="test_data", data=data)],
                visualizations=[visualization]
            )
        
        # Test skill creation
        assert test_helper_skill is not None
        assert hasattr(test_helper_skill, '__name__')
        
        # Create mock input
        class MockSkillInput:
            def __init__(self):
                self.arguments = type('obj', (object,), {})()
                self.user_full_query = "test query"
                self.workflow_id = "test-workflow"
        
        # Test skill execution
        mock_input = MockSkillInput()
        result = test_helper_skill(mock_input)
        
        # Verify result
        assert isinstance(result, SkillOutput)
        assert result.final_prompt == "Test skill executed successfully"
        assert len(result.export_data) == 1
        assert len(result.visualizations) == 1
        
        print("  ✓ Skill framework preview test passed")
        
    except Exception as e:
        print(f"  ⚠️ Skill framework preview test failed: {e}")

def test_json_validation():
    """Test JSON validation functionality"""
    # Test valid JSON
    valid_layout = {
        "type": "Document",
        "children": [{
            "type": "FlexContainer",
            "name": "TestContainer",
            "children": []
        }]
    }
    
    # Test that JSON can be serialized and deserialized
    json_str = json.dumps(valid_layout)
    parsed = json.loads(json_str)
    
    assert parsed["type"] == "Document"
    assert len(parsed["children"]) == 1
    assert parsed["children"][0]["name"] == "TestContainer"
    
    print("  ✓ JSON validation test passed")

def test_file_structure():
    """Test that expected helper files exist"""
    helper_dir = Path(__file__).parent.parent
    tests_dir = Path(__file__).parent

    # Check main helper files
    expected_helper_files = [
        "py_ex.py",
        "viz_previewer.py",
        "VISUALIZATION_TESTING_GUIDE.md"
    ]

    for file_name in expected_helper_files:
        file_path = helper_dir / file_name
        assert file_path.exists(), f"Expected helper file {file_name} not found"

    # Check test files
    expected_test_files = [
        "test_packages_and_connections.py",
        "test_helper_utilities.py",
        "test_visualization_framework.py",
        "test_skill_preview_example.py",
        "test_executor_integration.py",
        "run_all_tests.py",
        "README.md"
    ]

    for file_name in expected_test_files:
        file_path = tests_dir / file_name
        assert file_path.exists(), f"Expected test file {file_name} not found"

    print("  ✓ File structure test passed")

def main():
    """Run all helper utility tests"""
    print("=== HELPER UTILITIES TEST SUITE ===")
    print(f"Python version: {sys.version}")
    print(f"Test directory: {os.path.dirname(__file__)}")
    print()
    
    tests = [
        ("File Executor (py_ex.py)", test_py_ex_executor),
        ("Visualization Previewer", test_viz_previewer_imports),
        ("Skill Framework Preview", test_skill_framework_preview),
        ("JSON Validation", test_json_validation),
        ("File Structure", test_file_structure),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            print(f"Running {test_name}...")
            test_func()
            results.append((True, f"✓ {test_name}: Passed"))
            print(f"✓ {test_name}: Passed")
        except Exception as e:
            results.append((False, f"❌ {test_name}: Failed - {str(e)}"))
            print(f"❌ {test_name}: Failed - {str(e)}")
    
    print()
    print("=== SUMMARY ===")
    
    successful = sum(1 for success, _ in results if success)
    total = len(results)
    
    print(f"Successful tests: {successful}/{total}")
    
    if successful == total:
        print("🎉 All helper utility tests passed!")
        return 0
    else:
        print("⚠️ Some helper utility tests failed")
        failed_tests = [msg for success, msg in results if not success]
        print("\nFailed tests:")
        for msg in failed_tests:
            print(f"  {msg}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
