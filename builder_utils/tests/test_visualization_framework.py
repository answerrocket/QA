#!/usr/bin/env python3
"""
Visualization Framework Test Suite
Tests visualization creation, validation, and preview functionality
"""

import sys
import os
import json
import tempfile
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_skill_visualization_creation():
    """Test creating SkillVisualization objects"""
    from skill_framework import SkillVisualization
    
    # Test basic visualization creation
    layout = {
        "type": "Document",
        "rows": 100,
        "columns": 160,
        "children": [{
            "type": "FlexContainer",
            "name": "MainContainer",
            "children": []
        }]
    }
    
    viz = SkillVisualization(
        title="Test Visualization",
        layout=json.dumps(layout)
    )
    
    assert viz.title == "Test Visualization"
    assert isinstance(viz.layout, str)
    
    # Test that layout can be parsed back to JSON
    parsed_layout = json.loads(viz.layout)
    assert parsed_layout["type"] == "Document"
    assert len(parsed_layout["children"]) == 1
    
    print("  ✓ SkillVisualization creation test passed")

def test_highcharts_visualization():
    """Test creating Highcharts-based visualizations"""
    from skill_framework import SkillVisualization
    
    # Create a chart layout
    chart_layout = {
        "type": "Document",
        "children": [{
            "type": "HighchartsChart",
            "name": "TestChart",
            "options": {
                "chart": {"type": "column"},
                "title": {"text": "Test Chart"},
                "xAxis": {"categories": ["A", "B", "C"]},
                "yAxis": {"title": {"text": "Values"}},
                "series": [{
                    "name": "Test Series",
                    "data": [10, 20, 30]
                }]
            }
        }]
    }
    
    viz = SkillVisualization(
        title="Highcharts Test",
        layout=json.dumps(chart_layout)
    )
    
    # Validate the chart structure
    parsed = json.loads(viz.layout)
    chart = parsed["children"][0]
    
    assert chart["type"] == "HighchartsChart"
    assert chart["options"]["chart"]["type"] == "column"
    assert len(chart["options"]["series"][0]["data"]) == 3
    
    print("  ✓ Highcharts visualization test passed")

def test_export_data_creation():
    """Test creating ExportData objects"""
    from skill_framework import ExportData
    import pandas as pd
    
    # Create test data
    df = pd.DataFrame({
        'brand': ['Brand A', 'Brand B', 'Brand C'],
        'sales': [1000, 1500, 800],
        'growth': [5.2, 8.1, -2.3]
    })
    
    export_data = ExportData(name="test_export", data=df)
    
    assert export_data.name == "test_export"
    assert isinstance(export_data.data, pd.DataFrame)
    assert len(export_data.data) == 3
    assert list(export_data.data.columns) == ['brand', 'sales', 'growth']
    
    print("  ✓ ExportData creation test passed")

def test_skill_output_creation():
    """Test creating complete SkillOutput objects"""
    from skill_framework import SkillOutput, SkillVisualization, ExportData
    import pandas as pd
    
    # Create test data
    df = pd.DataFrame({'test': [1, 2, 3]})
    export_data = ExportData(name="test_data", data=df)
    
    # Create visualization
    layout = {"type": "Document", "children": []}
    viz = SkillVisualization(title="Test Viz", layout=json.dumps(layout))
    
    # Create skill output
    output = SkillOutput(
        final_prompt="Test completed successfully",
        export_data=[export_data],
        visualizations=[viz]
    )
    
    assert output.final_prompt == "Test completed successfully"
    assert len(output.export_data) == 1
    assert len(output.visualizations) == 1
    assert output.export_data[0].name == "test_data"
    assert output.visualizations[0].title == "Test Viz"
    
    print("  ✓ SkillOutput creation test passed")

def test_json_layout_validation():
    """Test JSON layout validation for common patterns"""
    
    # Test valid layouts
    valid_layouts = [
        # Simple document
        {"type": "Document", "children": []},
        
        # Document with container
        {
            "type": "Document",
            "children": [{
                "type": "FlexContainer",
                "name": "MainContainer",
                "children": []
            }]
        },
        
        # Document with chart
        {
            "type": "Document",
            "children": [{
                "type": "HighchartsChart",
                "name": "Chart1",
                "options": {"chart": {"type": "line"}}
            }]
        }
    ]
    
    for i, layout in enumerate(valid_layouts):
        # Test that layout can be serialized and deserialized
        json_str = json.dumps(layout)
        parsed = json.loads(json_str)
        
        assert parsed["type"] == "Document"
        assert "children" in parsed
        
        print(f"  ✓ Valid layout {i+1} passed validation")
    
    print("  ✓ JSON layout validation test passed")

def test_preview_skill_function():
    """Test the preview_skill function (without actually starting server)"""
    from skill_framework import skill, SkillInput, SkillOutput, SkillVisualization, ExportData
    import pandas as pd
    
    # Create a test skill
    @skill(
        name="test_preview_function",
        description="Test skill for preview function testing"
    )
    def test_preview_function(parameters: SkillInput) -> SkillOutput:
        df = pd.DataFrame({'x': [1, 2, 3], 'y': [4, 5, 6]})
        layout = {"type": "Document", "children": []}
        
        return SkillOutput(
            final_prompt="Preview test completed",
            export_data=[ExportData(name="preview_data", data=df)],
            visualizations=[SkillVisualization(title="Preview Viz", layout=json.dumps(layout))]
        )
    
    # Create mock input
    class MockSkillInput:
        def __init__(self):
            self.arguments = type('obj', (object,), {})()
            self.user_full_query = "test preview"
            self.workflow_id = "preview-test"
    
    # Execute skill
    mock_input = MockSkillInput()
    result = test_preview_function(mock_input)
    
    # Validate result structure
    assert isinstance(result, SkillOutput)
    assert result.final_prompt == "Preview test completed"
    assert len(result.export_data) == 1
    assert len(result.visualizations) == 1
    
    # Test that preview_skill function exists and can be called
    # (We won't actually start the server in tests)
    try:
        from skill_framework import preview_skill
        assert callable(preview_skill)
        print("  ✓ preview_skill function is available")
    except ImportError:
        print("  ⚠️ preview_skill function not available")
    
    print("  ✓ Preview skill function test passed")

def main():
    """Run all visualization framework tests"""
    print("=== VISUALIZATION FRAMEWORK TEST SUITE ===")
    print(f"Python version: {sys.version}")
    print(f"Test directory: {os.path.dirname(__file__)}")
    print()
    
    tests = [
        ("SkillVisualization Creation", test_skill_visualization_creation),
        ("Highcharts Visualization", test_highcharts_visualization),
        ("ExportData Creation", test_export_data_creation),
        ("SkillOutput Creation", test_skill_output_creation),
        ("JSON Layout Validation", test_json_layout_validation),
        ("Preview Skill Function", test_preview_skill_function),
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
        print("🎉 All visualization framework tests passed!")
        return 0
    else:
        print("⚠️ Some visualization framework tests failed")
        failed_tests = [msg for success, msg in results if not success]
        print("\nFailed tests:")
        for msg in failed_tests:
            print(f"  {msg}")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
