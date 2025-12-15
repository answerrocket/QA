import json
from skill_framework import skill, SkillOutput, SkillParameter, SkillInput, SkillVisualization
from skill_framework.layouts import wire_layout

DEFAULT_LAYOUT = """{
  "layoutJson": {
    "type": "Canvas",
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
    "children": []
  },
  "inputVariables": []
}
"""

@skill(
    name="viz_parameter_render",
    description="Renders a preset visualization layout with hotel brand performance data",
    parameters=[
            SkillParameter(
                name="viz_layout",
                parameter_type="visualization",
                description="Viz Layout",
            ),
            SkillParameter(
                name="viz_ppt_layout",
                parameter_type="visualization",
                description="Viz PPT Layout",
            )
        ]

)
def viz_parameter_render(skill_input: SkillInput) -> SkillOutput:
    """Renders a visualization demonstrating the dynamic-layout framework."""

    viz_layout = skill_input.arguments.viz_layout
    viz_ppt_layout = skill_input.arguments.viz_ppt_layout

    if viz_layout:
        raw_layout = json.loads(viz_layout)
        layout = {"layoutJson": raw_layout, "inputVariables": []}
    else:
        layout = json.loads(DEFAULT_LAYOUT)
    layout_json_string = wire_layout(layout, input_values={})

    if viz_ppt_layout:
        raw_ppt_layout = json.loads(viz_ppt_layout)
        ppt_layout = {"layoutJson": raw_ppt_layout, "inputVariables": []}
    else:
        ppt_layout = json.loads(DEFAULT_LAYOUT)
    ppt_layout_json_string = wire_layout(ppt_layout, input_values={})

    # Wrap in SkillVisualization
    visualization = SkillVisualization(
        title="Visualization Renderer",
        layout=layout_json_string
    )

    return SkillOutput(
        final_prompt="Here is the visualization you requested.",
        visualizations=[visualization],
        ppt_slides=[ppt_layout_json_string]
    )
