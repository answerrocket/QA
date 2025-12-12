import json
import pandas as pd
from skill_framework import skill, SkillInput, SkillOutput, SkillVisualization, ExportData
from skill_framework.layouts import wire_layout

VIZ_LAYOUT = """
[
{
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
            "height": "max-content",
            "padding": "15px",
            "gap": "20px"
        },
        "children": [
            {
                "name": "CardContainer0",
                "type": "CardContainer",
                "children": "",
                "minHeight": "80px",
                "rows": 2,
                "columns": 1,
                "style": {
                    "padding": "10px",
                    "fontFamily": "Arial"
                },
                "hidden": false
            },
            {
                "name": "mainTitle",
                "type": "Header",
                "row": 1,
                "column": 1,
                "width": 120,
                "height": 1,
                "style": {
                    "textAlign": "left",
                    "fontSize": "20px",
                    "fontWeight": "bold",
                    "color": "#333"
                },
                "text": "MDS for Hilton, Airbnb, Best Western | Among Gen Z",
                "parentId": "CardContainer0"
            },
            {
                "name": "subTitle",
                "type": "Header",
                "row": 5,
                "column": 1,
                "width": 120,
                "height": 12,
                "style": {
                    "textAlign": "left",
                    "fontSize": "14px",
                    "color": "#888"
                },
                "text": "2025-01-01 to 2025-12-31",
                "parentId": "CardContainer0"
            },
            {
                "name": "CardContainer2",
                "type": "CardContainer",
                "children": "",
                "minHeight": "40px",
                "rows": 1,
                "columns": 34,
                "maxHeight": "40px",
                "style": {
                    "borderRadius": "6.197px",
                    "background": "var(--Blue-50, #EFF6FF)",
                    "padding": "10px",
                    "paddingLeft": "20px",
                    "paddingRight": "20px"
                },
                "hidden": true
            },
            {
                "name": "Header2",
                "type": "Header",
                "width": 32,
                "children": "",
                "text": "<span style='font-family: Arial; margin-left: 5px;'>Growth is not available for the complete analysis period. This might impact the results</span>",
                "style": {
                    "fontSize": "14px",
                    "fontWeight": "normal",
                    "textAlign": "left",
                    "verticalAlign": "start",
                    "color": "#1D4ED8",
                    "border": "null",
                    "textDecoration": "null",
                    "writingMode": "horizontal-tb",
                    "alignItems": "start",
                    "fontFamily": ""
                },
                "parentId": "CardContainer2",
                "hidden": false
            },
            {
                "name": "DataTable1",
                "type": "DataTable",
                "showBorders": true,
                "columnBorders": true,
                "rowBorders": true,
                "columns": [
                    {
                        "name": "MDS",
                        "group": " ",
                        "style": {
                            "text-align": "left"
                        }
                    },
                    {
                        "name": "Current Score",
                        "group": "Hilton",
                        "style": {
                            "text-align": "center"
                        }
                    },
                    {
                        "name": "% Change",
                        "group": "Hilton",
                        "style": {
                            "text-align": "center"
                        }
                    },
                    {
                        "name": "Brand Change Vs Hilton",
                        "group": "Hilton",
                        "style": {
                            "text-align": "center"
                        }
                    },
                    {
                        "name": "Current Score",
                        "group": "Airbnb",
                        "style": {
                            "text-align": "center"
                        }
                    },
                    {
                        "name": "% Change",
                        "group": "Airbnb",
                        "style": {
                            "text-align": "center"
                        }
                    },
                    {
                        "name": "Brand Change Vs Hilton",
                        "group": "Airbnb",
                        "style": {
                            "text-align": "center"
                        }
                    },
                    {
                        "name": "Current Score",
                        "group": "Best Western",
                        "style": {
                            "text-align": "center"
                        }
                    },
                    {
                        "name": "% Change",
                        "group": "Best Western",
                        "style": {
                            "text-align": "center"
                        }
                    },
                    {
                        "name": "Brand Change Vs Hilton",
                        "group": "Best Western",
                        "style": {
                            "text-align": "center"
                        }
                    }
                ],
                "data": [
                    [
                        "Unaided Awareness",
                        "22%",
                        "-6%",
                        "0%",
                        "12%",
                        "+1%",
                        "-10% ↓",
                        "2%",
                        "-2%",
                        "-20% ↓"
                    ],
                    [
                        "Total Brand Awareness",
                        "94%",
                        "-1%",
                        "0%",
                        "94%",
                        "-2%",
                        "0%",
                        "2%",
                        "-2%",
                        "-92% ↓"
                    ],
                    [
                        "Total Consideration",
                        "72%",
                        "+1%",
                        "0%",
                        "67%",
                        "+2%",
                        "-5%",
                        "0%",
                        "0%",
                        "-72% ↓"
                    ],
                    [
                        "Past 12 Month Usage",
                        "40%",
                        "+2%",
                        "0%",
                        "38%",
                        "-1%",
                        "-2%",
                        "0%",
                        "0%",
                        "-40% ↓"
                    ]
                ],
                "styles": {
          "th": {
            "fontSize": "13px",
            "fontWeight": "",
            "padding": "16px 8px",
            "position": "sticky",
            "top": "0",
            "backgroundColor": "#f5f5f5",
            "borderTop": "1px solid #ddd",
            "borderBottom": "2px solid #ddd",
            "borderLeft": "1px solid #ddd",
            "borderRight": "1px solid #ddd"
          },
          "td": {
            "fontSize": "13px",
            "fontWeight": "",
            "padding": "18px 12px",
            "borderBottom": "1px solid #ddd"
          },
          "table": {
            "borderCollapse": "separate",
            "borderSpacing": "0"
          }
        },
                "hidden": false,
                "footer": "<span style='color: green'>&#9650;</span><span style='color: red'>▼</span>Significantly higher / lower at CI of 95%, Compared Vs Previous Year Same Period",
        "extraStyles": "max-height: 800px; overflow-y: auto; display: block;"
            },
            {
                "name": "CardContainer1",
                "type": "FlexContainer",
                "children": "",
                "direction": "column",
                "minHeight": "",
                "maxHeight": "",
                "style": {
                    "borderRadius": "11.911px",
                    "background": "var(--White, #FFF)",
                    "box-shadow": "0px 0px 8.785px 0px rgba(0, 0, 0, 0.10) inset",
                    "padding": "10px",
                    "fontFamily": "Arial"
                },
                "flexDirection": "row",
                "hidden": false
            },
            {
                "name": "Header1",
                "type": "Header",
                "children": "",
                "text": "Insights",
                "style": {
                    "fontSize": "27px",
                    "fontWeight": "700",
                    "textAlign": "left",
                    "verticalAlign": "start",
                    "color": "#000000",
                    "backgroundColor": "#ffffff",
                    "border": "null",
                    "textDecoration": "null",
                    "writingMode": "horizontal-tb",
                    "borderBottom": "solid #DDD 2px"
                },
                "parentId": "CardContainer1",
                "flex": "",
                "hidden": false
            },
            {
                "name": "Markdown0",
                "type": "Markdown",
                "children": "",
                "text": "**MDS for Hilton**- **Unaided Awareness**: Hilton's Unaided Awareness score is 30%, showing a 2% increase from the previous period, though not significant.- **Total Brand Awareness**: Hilton maintains a Total Brand Awareness score of 96%, with no change from the previous period.- **Total Consideration**: Hilton's Total Consideration score is 71%, reflecting a 1% increase from the previous period, but not significant.- **Past 12 Month Usage**: Hilton's Past 12 Month Usage score remains stable at 34%, with no change from the previous period.",
                "style": {
                    "color": "#555",
                    "backgroundColor": "#ffffff",
                    "border": "null",
                    "fontSize": "15px"
                },
                "parentId": "CardContainer1",
                "flex": "",
                "hidden": false
            }
        ]
    },
    "inputVariables": [
        {
            "name": "headline",
            "isRequired": false,
            "defaultValue": null,
            "targets": [
                {
                    "elementName": "mainTitle",
                    "fieldName": "text"
                }
            ]
        },
        {
            "name": "sub_headline",
            "isRequired": false,
            "defaultValue": null,
            "targets": [
                {
                    "elementName": "subTitle",
                    "fieldName": "text"
                }
            ]
        },
        {
            "name": "col_defs",
            "isRequired": false,
            "defaultValue": null,
            "targets": [
                {
                    "elementName": "DataTable1",
                    "fieldName": "columns"
                }
            ]
        },
        {
            "name": "data",
            "isRequired": false,
            "defaultValue": null,
            "targets": [
                {
                    "elementName": "DataTable1",
                    "fieldName": "data"
                }
            ]
        },
        {
            "name": "table_footer",
            "isRequired": false,
            "defaultValue": null,
            "targets": [
                {
                    "elementName": "DataTable1",
                    "fieldName": "footer"
                }
            ]
        },
        {
            "name": "exec_summary",
            "isRequired": false,
            "defaultValue": null,
            "targets": [
                {
                    "elementName": "Markdown0",
                    "fieldName": "text"
                }
            ]
        }
    ]
}]
"""

@skill(
    name="table_block_diagnostics",
    description="A skill to diagnose the table block using VIZ_LAYOUT",
)
def table_block_diagnostics(skill_input: SkillInput) -> SkillOutput:
    # Parse the VIZ_LAYOUT JSON
    layout_config = json.loads(VIZ_LAYOUT)[0]

    # Create dummy data matching the layout's expected structure
    # The layout expects: headline, sub_headline, col_defs, data, table_footer, exec_summary

    # Dummy column definitions for 5 brands with 3 metrics each
    col_defs = [
        {"name": "MDS", "group": " ", "style": {"text-align": "left"}},
        {"name": "Current Score", "group": "Brand A", "style": {"text-align": "center"}},
        {"name": "% Change", "group": "Brand A", "style": {"text-align": "center"}},
        {"name": "Vs Competitor", "group": "Brand A", "style": {"text-align": "center"}},
        {"name": "Current Score", "group": "Brand B", "style": {"text-align": "center"}},
        {"name": "% Change", "group": "Brand B", "style": {"text-align": "center"}},
        {"name": "Vs Competitor", "group": "Brand B", "style": {"text-align": "center"}},
        {"name": "Current Score", "group": "Brand C", "style": {"text-align": "center"}},
        {"name": "% Change", "group": "Brand C", "style": {"text-align": "center"}},
        {"name": "Vs Competitor", "group": "Brand C", "style": {"text-align": "center"}},
        {"name": "Current Score", "group": "Brand D", "style": {"text-align": "center"}},
        {"name": "% Change", "group": "Brand D", "style": {"text-align": "center"}},
        {"name": "Vs Competitor", "group": "Brand D", "style": {"text-align": "center"}},
        {"name": "Current Score", "group": "Brand E", "style": {"text-align": "center"}},
        {"name": "% Change", "group": "Brand E", "style": {"text-align": "center"}},
        {"name": "Vs Competitor", "group": "Brand E", "style": {"text-align": "center"}},
    ]

    # Dummy table data rows (16 MDS metrics x 5 brands)
    dummy_data = [
        ["Unaided Awareness", "85%", "+3%", "0%", "72%", "-2%", "-13% ↓", "65%", "+1%", "-20% ↓", "58%", "+4%", "-27% ↓", "51%", "-1%", "-34% ↓"],
        ["Total Brand Awareness", "91%", "+1%", "0%", "88%", "-1%", "-3%", "79%", "+2%", "-12% ↓", "82%", "+3%", "-9% ↓", "75%", "+1%", "-16% ↓"],
        ["Total Consideration", "68%", "-2%", "0%", "71%", "+4%", "+3% ↑", "55%", "-3%", "-13% ↓", "61%", "+2%", "-7% ↓", "49%", "-1%", "-19% ↓"],
        ["Past 12 Month Usage", "45%", "+5%", "0%", "42%", "+2%", "-3%", "38%", "-1%", "-7% ↓", "35%", "+3%", "-10% ↓", "31%", "+1%", "-14% ↓"],
        ["Purchase Intent", "52%", "+4%", "0%", "48%", "+1%", "-4%", "41%", "-2%", "-11% ↓", "44%", "+2%", "-8% ↓", "37%", "-1%", "-15% ↓"],
        ["Brand Preference", "39%", "+2%", "0%", "35%", "-3%", "-4%", "28%", "+1%", "-11% ↓", "32%", "+4%", "-7% ↓", "25%", "-2%", "-14% ↓"],
        ["Net Promoter Score", "62%", "+6%", "0%", "54%", "+2%", "-8% ↓", "47%", "-1%", "-15% ↓", "51%", "+3%", "-11% ↓", "43%", "+1%", "-19% ↓"],
        ["Customer Satisfaction", "78%", "+1%", "0%", "75%", "+3%", "-3%", "69%", "+2%", "-9% ↓", "72%", "+1%", "-6%", "66%", "-1%", "-12% ↓"],
        ["Brand Trust", "81%", "+2%", "0%", "76%", "-1%", "-5%", "71%", "+1%", "-10% ↓", "74%", "+2%", "-7% ↓", "68%", "+1%", "-13% ↓"],
        ["Value Perception", "59%", "-1%", "0%", "63%", "+5%", "+4% ↑", "52%", "-2%", "-7% ↓", "56%", "+3%", "-3%", "48%", "+1%", "-11% ↓"],
        ["Quality Perception", "83%", "+3%", "0%", "79%", "+1%", "-4%", "74%", "+2%", "-9% ↓", "77%", "+2%", "-6%", "71%", "-1%", "-12% ↓"],
        ["Innovation Score", "67%", "+7%", "0%", "58%", "+4%", "-9% ↓", "49%", "+3%", "-18% ↓", "53%", "+5%", "-14% ↓", "44%", "+2%", "-23% ↓"],
        ["Emotional Connection", "55%", "+4%", "0%", "51%", "+2%", "-4%", "43%", "-1%", "-12% ↓", "47%", "+3%", "-8% ↓", "39%", "+1%", "-16% ↓"],
        ["Brand Loyalty", "61%", "+3%", "0%", "57%", "+1%", "-4%", "49%", "+2%", "-12% ↓", "53%", "+2%", "-8% ↓", "45%", "-1%", "-16% ↓"],
        ["Recommendation Likelihood", "58%", "+5%", "0%", "52%", "+3%", "-6%", "44%", "+1%", "-14% ↓", "48%", "+4%", "-10% ↓", "41%", "+2%", "-17% ↓"],
        ["Price Sensitivity", "42%", "-2%", "0%", "47%", "+1%", "+5% ↑", "53%", "+3%", "+11% ↑", "49%", "+2%", "+7% ↑", "56%", "+4%", "+14% ↑"],
    ]

    # Dummy executive summary
    exec_summary = """**Brand Performance Summary (5 Brands, 16 MDS Metrics)**

- **Brand A**: Market leader with strongest scores across all 16 metrics. Top performer in Brand Trust (81%), Total Brand Awareness (91%), Quality Perception (83%), and Customer Satisfaction (78%). Innovation Score showing strongest growth (+7%). Lowest Price Sensitivity (42%) indicates premium positioning.
- **Brand B**: Strong challenger with competitive Brand Awareness (88%) and improving Value Perception (+5%). Shows strength in Total Consideration (+4%) outperforming Brand A. Net Promoter Score trails by 8 points.
- **Brand C**: Mid-tier performer with consistent gaps of 10-20% vs Brand A. Highest Price Sensitivity (53%) among top 3 brands suggests value-focused positioning. Needs improvement in Unaided Awareness (65%) and Brand Preference (28%).
- **Brand D**: Emerging competitor showing growth momentum with strong gains in Innovation Score (+5%) and Brand Preference (+4%). Closing gap on Brand C in most metrics.
- **Brand E**: Trailing brand with largest gaps vs market leader (20-35% behind Brand A). Highest Price Sensitivity (56%) indicates budget positioning. Recommendation Likelihood and Brand Loyalty need strategic focus.

**Key Insights:**
1. Brand A dominates premium segment with trust, quality, and low price sensitivity
2. Brand B positioned as strong value alternative with growth in consideration metrics
3. Brands C-E show opportunity in emotional connection and brand loyalty improvement
4. Price Sensitivity inversely correlates with brand strength - opportunity for value messaging"""

    # Wire the layout with dummy data
    rendered_layout = wire_layout(layout_config, {
        "headline": "Brand Comparison Dashboard | Dummy Data Demo",
        "sub_headline": "2024-01-01 to 2024-12-31",
        "col_defs": col_defs,
        "data": dummy_data,
        "table_footer": "<span style='color: green'>▲</span><span style='color: red'>▼</span> Significantly higher/lower at 95% CI",
        "exec_summary": exec_summary
    })

    # Create visualization
    visualization = SkillVisualization(
        title="Table Block Diagnostics",
        layout=rendered_layout
    )

    # Create dummy DataFrame for export (16 MDS metrics x 5 brands)
    df = pd.DataFrame({
        'MDS': [
            'Unaided Awareness', 'Total Brand Awareness', 'Total Consideration',
            'Past 12 Month Usage', 'Purchase Intent', 'Brand Preference',
            'Net Promoter Score', 'Customer Satisfaction', 'Brand Trust',
            'Value Perception', 'Quality Perception', 'Innovation Score',
            'Emotional Connection', 'Brand Loyalty', 'Recommendation Likelihood', 'Price Sensitivity'
        ],
        'Brand_A_Score': [85, 91, 68, 45, 52, 39, 62, 78, 81, 59, 83, 67, 55, 61, 58, 42],
        'Brand_A_Change': [3, 1, -2, 5, 4, 2, 6, 1, 2, -1, 3, 7, 4, 3, 5, -2],
        'Brand_B_Score': [72, 88, 71, 42, 48, 35, 54, 75, 76, 63, 79, 58, 51, 57, 52, 47],
        'Brand_B_Change': [-2, -1, 4, 2, 1, -3, 2, 3, -1, 5, 1, 4, 2, 1, 3, 1],
        'Brand_C_Score': [65, 79, 55, 38, 41, 28, 47, 69, 71, 52, 74, 49, 43, 49, 44, 53],
        'Brand_C_Change': [1, 2, -3, -1, -2, 1, -1, 2, 1, -2, 2, 3, -1, 2, 1, 3],
        'Brand_D_Score': [58, 82, 61, 35, 44, 32, 51, 72, 74, 56, 77, 53, 47, 53, 48, 49],
        'Brand_D_Change': [4, 3, 2, 3, 2, 4, 3, 1, 2, 3, 2, 5, 3, 2, 4, 2],
        'Brand_E_Score': [51, 75, 49, 31, 37, 25, 43, 66, 68, 48, 71, 44, 39, 45, 41, 56],
        'Brand_E_Change': [-1, 1, -1, 1, -1, -2, 1, -1, 1, 1, -1, 2, 1, -1, 2, 4]
    })

    export_data = ExportData(
        name="brand_comparison_data",
        data=df
    )

    return SkillOutput(
        visualizations=[visualization],
        export_data=[export_data],
        final_prompt="Here is the brand comparison dashboard with dummy data demonstrating the VIZ_LAYOUT template."
    )
