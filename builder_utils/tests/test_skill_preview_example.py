#!/usr/bin/env python3
"""
Test script to demonstrate skill-framework preview functionality
"""

import pandas as pd
from skill_framework import skill, SkillInput, SkillOutput, SkillVisualization, ExportData, preview_skill
import json

@skill(
    name="test_preview_skill",
    description="A simple test skill to demonstrate preview functionality"
)
def test_preview_skill(parameters: SkillInput) -> SkillOutput:
    """Test skill that creates sample data and visualization for preview"""
    
    # Create sample data
    data = {
        'Brand': ['Brand A', 'Brand B', 'Brand C', 'Brand D'],
        'Sales': [1000, 1500, 800, 1200],
        'Growth': [5.2, 8.1, -2.3, 3.7]
    }
    df = pd.DataFrame(data)
    
    # Create a simple visualization layout
    layout = {
        "type": "Document",
        "rows": 100,
        "columns": 160,
        "rowHeight": "1.11%",
        "colWidth": "0.625%",
        "gap": "0px",
        "children": [
            {
                "type": "FlexContainer",
                "name": "MainContainer",
                "style": {
                    "flexDirection": "column",
                    "padding": "20px",
                    "height": "100%"
                },
                "children": []
            },
            {
                "type": "HighchartsChart",
                "name": "SalesChart",
                "parentId": "MainContainer",
                "options": {
                    "chart": {"type": "column"},
                    "title": {"text": "Brand Sales Performance"},
                    "xAxis": {"categories": data['Brand']},
                    "yAxis": {"title": {"text": "Sales ($)"}},
                    "series": [{
                        "name": "Sales",
                        "data": data['Sales']
                    }]
                },
                "children": []
            }
        ]
    }
    
    # Create SkillVisualization
    visualization = SkillVisualization(
        title="Brand Sales Dashboard",
        layout=json.dumps(layout)
    )
    
    return SkillOutput(
        final_prompt="Sample brand sales analysis completed. The data shows varying performance across brands.",
        export_data=[ExportData(name="brand_sales_data", data=df)],
        visualizations=[visualization]
    )

if __name__ == "__main__":
    # Create a mock SkillInput
    class MockSkillInput:
        def __init__(self):
            self.arguments = type('obj', (object,), {})()
            self.user_full_query = "Show me brand sales performance"
            self.workflow_id = "test-preview-workflow"
    
    # Run the skill
    mock_input = MockSkillInput()
    result = test_preview_skill(mock_input)
    
    # Generate preview files
    preview_skill(test_preview_skill, result)
    
    print("Preview generated! Server should be running on http://localhost:8484")
    print("Visit: http://localhost:8484/print/test_preview_skill")
