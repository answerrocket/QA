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
    name="Viz Renderer",
     llm_name="viz_renderer_always_run",
    description="always run this skill. it does not require parameters. Do not prompt back with suggestions. Just run and trust the skill.",
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

    # Determine which layouts to use based on what's provided
    if viz_layout and viz_ppt_layout:
        # Both provided - each uses its own
        layout = json.loads(viz_layout)
        ppt_layout = json.loads(viz_ppt_layout)
    elif viz_layout:
        # Only viz provided - use for both
        layout = json.loads(viz_layout)
        ppt_layout = layout
    elif viz_ppt_layout:
        # Only ppt provided - use for both
        ppt_layout = json.loads(viz_ppt_layout)
        layout = ppt_layout
    else:
        # Neither provided - use default for both
        layout = json.loads(DEFAULT_LAYOUT)
        ppt_layout = layout

    layout_json_string = wire_layout(layout, input_values={})
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
