import os
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from answer_rocket import AnswerRocketClient
from skill_framework import skill, SkillParameter, SkillInput, SkillOutput, SkillVisualization, ExportData, ExitFromSkillException
from skill_framework.layouts import wire_layout

@skill(
    name="large_df",
    description="output a large dataframe",
    parameters=[
    ]
)
def export_large_df(skill_input: SkillInput) -> SkillOutput:
    """Creates a sortable data table displaying top 100 rows"""
    # Generate full dataset
    df = pd.DataFrame({
        'id': range(1, 65001),
        'value': np.random.randint(0, 100, 65000),
        'category': np.random.choice(['A', 'B', 'C', 'D'], 65000),
        'score': np.random.uniform(0, 1, 65000)
    })

    # Take only top 100 rows for display
    df_display = df.head(100)

    # Create layout structure for table
    table_layout = {
        "inputVariables": [
            {
                "name": "title",
                "targets": [{"elementName": "Header0", "fieldName": "text"}]
            },
            {
                "name": "table_data",
                "targets": [{"elementName": "DataTable0", "fieldName": "data"}]
            },
            {
                "name": "table_columns",
                "targets": [{"elementName": "DataTable0", "fieldName": "columns"}]
            }
        ],
        "layoutJson": {
            "type": "Document",
            "rows": 90,
            "columns": 160,
            "rowHeight": "1.11%",
            "colWidth": "0.625%",
            "gap": "0px",
            "style": {
                "backgroundColor": "#ffffff",
                "width": "100%",
                "height": "100%"
            },
            "children": [
                {
                    "name": "FlexContainer0",
                    "type": "FlexContainer",
                    "row": 1,
                    "column": 1,
                    "width": 160,
                    "height": 88,
                    "minHeight": "250px",
                    "rows": 2,
                    "columns": 1,
                    "direction": "column"
                },
                {
                    "name": "Header0",
                    "type": "Header",
                    "text": "",
                    "style": {
                        "fontSize": "22px",
                        "fontWeight": "bold",
                        "textAlign": "left",
                        "verticalAlign": "start",
                        "color": "#000000",
                        "backgroundColor": "#ffffff",
                        "border": "none"
                    },
                    "parentId": "FlexContainer0",
                    "flex": ""
                },
                {
                    "name": "DataTable0",
                    "type": "DataTable",
                    "columns": [],
                    "data": [],
                    "parentId": "FlexContainer0",
                    "styles": {
                        "th": {
                            "fontSize": "13px",
                            "fontWeight": "bold",
                            "padding": "16px 8px",
                            "backgroundColor": "#F0F0F0",
                            "color": "#000000"
                        },
                        "td": {
                            "fontSize": "13px",
                            "padding": "18px 12px"
                        },
                        "alternateRowColor": "#f9f9f9",
                        "fontFamily": "Arial, sans-serif"
                    }
                }
            ]
        }
    }

    # Prepare data for wire_layout
    table_columns = [{"name": col} for col in df_display.columns]
    table_data = df_display.fillna('').to_numpy().tolist()

    # Wire the layout with data
    rendered_layout = wire_layout(table_layout, {
        "title": f"Top 100 Rows (Total: {len(df):,} rows)",
        "table_columns": table_columns,
        "table_data": table_data
    })

    # Create table visualization
    visualization = SkillVisualization(
        title="Data Table",
        layout=rendered_layout
    )

    # Export full dataset
    export_data = ExportData(
        name="large_df",
        data=df
    )

    return SkillOutput(
        visualizations=[visualization],
        export_data=[export_data],
        final_prompt=f"Here are the top 100 rows from the dataset (total rows: {len(df):,})"
    )
