import json
from skill_framework import skill, SkillOutput, SkillParameter, SkillInput
from skill_framework.layouts import wire_layout


@skill(
    name="viz_parameter_render",
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
    """Renders a visualization demonstrating the dynamic-layout framework."""

    viz_layout = skill_input.arguments.viz_layout

    layout = json.loads(viz_layout)

    visualization = wire_layout(layout, input_values={})

    return SkillOutput(
        final_prompt="Here is the visualization you requested.",
        visualizations=[visualization]
    )
