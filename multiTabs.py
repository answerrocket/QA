from skill_framework import skill, SkillParameter, SkillInput, SkillOutput,SkillVisualization
import json
LAYOUT = """
[
    {
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
                    "border-radius": "11.911px",
                    "background": "#2563EB",
                    "padding": "10px",
                    "fontFamily": "Arial"
                },
                "hidden": false
            },
            {
                "name": "Header0",
                "type": "Header",
                "children": "",
                "text": "Example Dynamic Layout",
                "style": {
                    "fontSize": "20px",
                    "fontWeight": "700",
                    "color": "#ffffff",
                    "textAlign": "left",
                    "alignItems": "center"
                },
                "parentId": "CardContainer0",
                "hidden": false
            },
            {
                "name": "Paragraph0",
                "type": "Paragraph",
                "children": "",
                "text": "Add a description here",
                "style": {
                    "fontSize": "15px",
                    "fontWeight": "normal",
                    "textAlign": "center",
                    "verticalAlign": "start",
                    "color": "#fafafa",
                    "border": "none",
                    "textDecoration": "none",
                    "writingMode": "horizontal-tb",
                    "alignItems": "center"
                },
                "parentId": "CardContainer0",
                "hidden": false
            },
            {
                "type": "HighchartsChart",
                "name": "HighchartsChart0",
                "children": [],
                "options": {
                    "chart": {
                        "type": "pie"
                    },
                    "title": {
                        "text": "Sample Highcharts"
                    },
                    "series": [
                        {
                            "name": "Series 1",
                            "colorByPoint": true,
                            "data": [
                                [
                                    "Category A",
                                    75
                                ],
                                [
                                    "Category B",
                                    20
                                ],
                                [
                                    "Category C",
                                    30
                                ],
                                [
                                    "Category D",
                                    62
                                ],
                                [
                                    "Category E",
                                    10
                                ]
                            ]
                        }
                    ]
                }
            },
            {
                "name": "Header1",
                "type": "Header",
                "children": "",
                "text": "Executive Summary",
                "style": {
                    "fontSize": "20px",
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
                "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. ",
                "style": {
                    "color": "#555",
                    "backgroundColor": "#ffffff",
                    "border": "null",
                    "fontSize": "15px"
                },
                "parentId": "CardContainer1",
                "flex": "",
                "hidden": false
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
            }
        ]
    },
    {
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
                    "border-radius": "11.911px",
                    "background": "#2563EB",
                    "padding": "10px",
                    "fontFamily": "Arial"
                },
                "hidden": false
            },
            {
                "name": "Header0",
                "type": "Header",
                "children": "",
                "text": "Example Dynamic Layout",
                "style": {
                    "fontSize": "20px",
                    "fontWeight": "700",
                    "color": "#ffffff",
                    "textAlign": "left",
                    "alignItems": "center"
                },
                "parentId": "CardContainer0",
                "hidden": false
            },
            {
                "name": "Paragraph0",
                "type": "Paragraph",
                "children": "",
                "text": "Add a description here",
                "style": {
                    "fontSize": "15px",
                    "fontWeight": "normal",
                    "textAlign": "center",
                    "verticalAlign": "start",
                    "color": "#fafafa",
                    "border": "none",
                    "textDecoration": "none",
                    "writingMode": "horizontal-tb",
                    "alignItems": "center"
                },
                "parentId": "CardContainer0",
                "hidden": false
            },
            {
                "type": "HighchartsChart",
                "name": "HighchartsChart0",
                "children": [],
                "options": {
                    "chart": {
                        "type": "line"
                    },
                    "title": {
                        "text": "Sample Highcharts"
                    },
                    "series": [
                        {
                            "name": "Series 1",
                            "colorByPoint": true,
                            "data": [
                                [
                                    "Category A",
                                    75
                                ],
                                [
                                    "Category B",
                                    20
                                ],
                                [
                                    "Category C",
                                    30
                                ],
                                [
                                    "Category D",
                                    62
                                ],
                                [
                                    "Category E",
                                    10
                                ]
                            ]
                        }
                    ]
                }
            },
            {
                "name": "Header1",
                "type": "Header",
                "children": "",
                "text": "Executive Summary",
                "style": {
                    "fontSize": "20px",
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
                "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. ",
                "style": {
                    "color": "#555",
                    "backgroundColor": "#ffffff",
                    "border": "null",
                    "fontSize": "15px"
                },
                "parentId": "CardContainer1",
                "flex": "",
                "hidden": false
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
            }
        ]
    },
    {
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
                    "border-radius": "11.911px",
                    "background": "#2563EB",
                    "padding": "10px",
                    "fontFamily": "Arial"
                },
                "hidden": false
            },
            {
                "name": "Header0",
                "type": "Header",
                "children": "",
                "text": "Example Dynamic Layout",
                "style": {
                    "fontSize": "20px",
                    "fontWeight": "400",
                    "color": "#ffffff",
                    "textAlign": "left",
                    "alignItems": "center",
                    "backgroundColor": "#db4343"
                },
                "parentId": "CardContainer0",
                "hidden": false
            },
            {
                "name": "Paragraph0",
                "type": "Paragraph",
                "children": "",
                "text": "Add a description here",
                "style": {
                    "fontSize": "15px",
                    "fontWeight": "normal",
                    "textAlign": "center",
                    "verticalAlign": "start",
                    "color": "#fafafa",
                    "border": "none",
                    "textDecoration": "none",
                    "writingMode": "horizontal-tb",
                    "alignItems": "center"
                },
                "parentId": "CardContainer0",
                "hidden": false
            },
            {
                "type": "HighchartsChart",
                "name": "HighchartsChart0",
                "children": [],
                "options": {
                    "chart": {
                        "type": "column"
                    },
                    "title": {
                        "text": "Sample Highcharts"
                    },
                    "series": [
                        {
                            "name": "Series 1",
                            "colorByPoint": true,
                            "data": [
                                [
                                    "Category A",
                                    75
                                ],
                                [
                                    "Category B",
                                    20
                                ],
                                [
                                    "Category C",
                                    30
                                ],
                                [
                                    "Category D",
                                    62
                                ],
                                [
                                    "Category E",
                                    10
                                ]
                            ]
                        }
                    ]
                }
            },
            {
                "name": "Header1",
                "type": "Header",
                "children": "",
                "text": "Executive Summary",
                "style": {
                    "fontSize": "20px",
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
                "text": "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. ",
                "style": {
                    "color": "#555",
                    "backgroundColor": "#ffffff",
                    "border": "null",
                    "fontSize": "15px"
                },
                "parentId": "CardContainer1",
                "flex": "",
                "hidden": false
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
            }
        ]
    },
    {
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
                    "border-radius": "11.911px",
                    "background": "#2563EB",
                    "padding": "10px",
                    "fontFamily": "Arial"
                },
                "hidden": false
            },
            {
                "name": "Header0",
                "type": "Header",
                "children": "",
                "text": "Dynamic, Affinity, Aided Awareness for Hilton",
                "style": {
                    "fontSize": "20px",
                    "fontWeight": "700",
                    "color": "#ffffff",
                    "textAlign": "left",
                    "alignItems": "center"
                },
                "parentId": "CardContainer0",
                "hidden": false
            },
            {
                "name": "Paragraph0",
                "type": "Paragraph",
                "children": "",
                "text": "Correlation Analysis",
                "style": {
                    "fontSize": "15px",
                    "fontWeight": "normal",
                    "textAlign": "center",
                    "verticalAlign": "start",
                    "color": "#fafafa",
                    "border": "none",
                    "textDecoration": "none",
                    "writingMode": "horizontal-tb",
                    "alignItems": "center"
                },
                "parentId": "CardContainer0",
                "hidden": false
            },
            {
                "name": "Header1",
                "type": "Header",
                "children": "",
                "text": "Executive Summary",
                "style": {
                    "fontSize": "20px",
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
                "text": "No Insights.",
                "style": {
                    "color": "#555",
                    "backgroundColor": "#ffffff",
                    "border": "null",
                    "fontSize": "15px"
                },
                "parentId": "CardContainer1",
                "flex": "",
                "hidden": false
            },
            {
                "name": "HighchartsChart0",
                "type": "HighchartsChart",
                "minHeight": "400px",
                "options": {
                    "chart": {
                        "type": "heatmap",
                        "polar": false
                    },
                    "title": {
                        "text": "",
                        "style": {
                            "fontSize": "20px"
                        }
                    },
                    "colorAxis": {
                        "min": -1,
                        "max": 1,
                        "stops": [
                            [
                                0,
                                "#f65657"
                            ],
                            [
                                0.1,
                                "#fd8179"
                            ],
                            [
                                0.2,
                                "#ff9f97"
                            ],
                            [
                                0.3,
                                "#ffbab3"
                            ],
                            [
                                0.4,
                                "#fedcd8"
                            ],
                            [
                                0.5,
                                "#f4f4f4"
                            ],
                            [
                                0.6,
                                "#d0e3d5"
                            ],
                            [
                                0.7,
                                "#abd1b8"
                            ],
                            [
                                0.8,
                                "#86be9b"
                            ],
                            [
                                0.9,
                                "#64ad81"
                            ],
                            [
                                1,
                                "#229359"
                            ]
                        ]
                    },
                    "xAxis": {
                        "categories": [
                            "Dynamic",
                            "Affinity",
                            "Aided Awareness"
                        ],
                        "title": {
                            "text": ""
                        }
                    },
                    "yAxis": {
                        "title": "",
                        "categories": [
                            "Aided Awareness",
                            "Affinity",
                            "Dynamic"
                        ]
                    },
                    "series": {
                        "name": "correlation",
                        "borderWidth": 1,
                        "dataLabels": {
                            "enabled": true,
                            "format": "{point.value:.2f}"
                        },
                        "tooltip": {
                            "headerFormat": "<span style=\\"color:{point.color}\\">●</span> <b>{point.xCategory}</b> vs <b>{point.yCategory}</b><br/>",
                            "pointFormat": "Correlation: {point.value:.2f}"
                        },
                        "data": [
                            {
                                "x": 0,
                                "y": 2,
                                "value": 1,
                                "xCategory": "Dynamic",
                                "yCategory": "Dynamic"
                            },
                            {
                                "x": 1,
                                "y": 2,
                                "value": 0.15,
                                "xCategory": "Affinity",
                                "yCategory": "Dynamic"
                            },
                            {
                                "x": 2,
                                "y": 2,
                                "value": -0.03,
                                "xCategory": "Aided Awareness",
                                "yCategory": "Dynamic"
                            },
                            {
                                "x": 0,
                                "y": 1,
                                "value": 0.15,
                                "xCategory": "Dynamic",
                                "yCategory": "Affinity"
                            },
                            {
                                "x": 1,
                                "y": 1,
                                "value": 1,
                                "xCategory": "Affinity",
                                "yCategory": "Affinity"
                            },
                            {
                                "x": 2,
                                "y": 1,
                                "value": -0.28,
                                "xCategory": "Aided Awareness",
                                "yCategory": "Affinity"
                            },
                            {
                                "x": 0,
                                "y": 0,
                                "value": -0.03,
                                "xCategory": "Dynamic",
                                "yCategory": "Aided Awareness"
                            },
                            {
                                "x": 1,
                                "y": 0,
                                "value": -0.28,
                                "xCategory": "Affinity",
                                "yCategory": "Aided Awareness"
                            },
                            {
                                "x": 2,
                                "y": 0,
                                "value": 1,
                                "xCategory": "Aided Awareness",
                                "yCategory": "Aided Awareness"
                            }
                        ]
                    },
                    "plotOptions": {
                        "column": {
                            "dataLabels": {
                                "enabled": false
                            },
                            "series": {
                                "animation": false
                            }
                        }
                    },
                    "legend": {
                        "align": "center",
                        "verticalAlign": "bottom"
                    }
                }
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
            }
        ]
    }
]
"""
@skill(
    name="multiTabs",
    description="An example skill",
    parameters=[
    ]
)
def multiTabs(parameters: SkillInput) -> SkillOutput:
    viz = []
    viz_list = json.loads(LAYOUT)

    for tab in viz_list:
        table = SkillVisualization(title="tab",
        layout=json.dumps(tab))
        viz.append(table)
    return SkillOutput(visualizations=viz)
