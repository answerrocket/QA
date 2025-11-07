import os
import json
import pandas as pd
import numpy as np
from dotenv import load_dotenv
from answer_rocket import AnswerRocketClient
from skill_framework import skill, SkillParameter, SkillInput, SkillOutput, SkillVisualization, ExportData, ExitFromSkillException

@skill(
    name="large_df",
    description="output a large dataframe",
    parameters=[
    ]
)
def export_large_df(skill_input: SkillInput) -> SkillOutput:
    """Creates a sortable data table with configurable dimensions and metrics"""
    df = pd.DataFrame({
        'id': range(1, 65001),
        'value': np.random.randint(0, 100, 65000),
        'category': np.random.choice(['A', 'B', 'C', 'D'], 65000),
        'score': np.random.uniform(0, 1, 65000)
    })
    visualization = SkillVisualization(
        title="large_df",
        layout=json.dumps({
            "type": "data_table",
            "data": df.to_dict(orient="records")
        })
    )
    export_data = ExportData(
        name="large_df",
        data=df
    )
        
    return SkillOutput(
        export_data=[export_data],
        final_prompt="large_df"
    )
