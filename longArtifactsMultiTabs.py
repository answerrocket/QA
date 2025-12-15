from skill_framework import skill, SkillParameter, SkillInput, SkillOutput,SkillVisualization

LAYOUT = """
{
  "type": "Document",
  "gap": "0px",
  "style": {
    "backgroundColor": "#ffffff",
    "width": "100%",
    "height": "max-content"
  },
  "children": [
    {
      "name": "DataTable0",
      "type": "DataTable",
      "columns": [
        {
          "name": "Column 1"
        }
      ],
      "data": [
        [
          "Row 1"
        ]
      ]
    }
  ]
}
"""
@skill(
    name="longArtifactsMultiTabs",
    description="An example skill",
    parameters=[
        SkillParameter(
            name="metric",
            constrained_to="metrics",
        )
    ]
)
def longArtifactsMultiTabs(parameters: SkillInput) -> SkillOutput:
    viz = []
    for i in range(10):
        table = SkillVisualization(title=f"Metrics Table {i}", 
        layout=LAYOUT)
        viz.append(table)
    return SkillOutput(visualizations=viz)
