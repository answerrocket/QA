"""
Viz Renderer Skill

This skill renders a predefined visualization layout showcasing hotel brand
performance comparison data. It demonstrates the dynamic-layout framework
with a canvas containing a header, markdown summary, and data table.
"""

import json
from skill_framework import skill, SkillOutput, SkillParameter, SkillInput
from skill_framework.layouts import wire_layout


@skill(
    name="viz_parameter_render",
    display_name="Viz Renderer",
    description="Renders a preset visualization layout with hotel brand performance data",
   parameters=[
        SkillParameter(
            name="viz_layout",
            parameter_type="visualization",
            description="Viz Layout",
        )
    ]

)
def viz_parameter_render(skill_input: SkillInput) -> SkillOutput:
    """
    Renders a visualization demonstrating the dynamic-layout framework.

    Returns a canvas layout containing:
    - Header with title
    - Markdown text with summary analysis
    - DataTable with brand performance metrics
    """

    # Create the data for the table
    viz_layout = skill_input.arguments.viz_layout

    layout = json.loads(viz_layout)    

    # Create the wired layout
    visualization = wire_layout(layout, input_variables={})

    return SkillOutput(
        final_prompt="Here is the visualization you requested.",
        visualizations=[visualization]
    )
