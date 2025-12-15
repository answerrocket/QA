import os
import json
import pandas as pd
from dotenv import load_dotenv
from answer_rocket import AnswerRocketClient
from skill_framework import skill, SkillParameter, SkillInput, SkillOutput, SkillVisualization, ExportData, ExitFromSkillException

@skill(
    name="basic_data_bar_chart",
    description="Creates a bar chart from dataset dimensions and metrics",
    parameters=[
        SkillParameter(
            name="dimension", 
            description="The dimension to group data by",
            constrained_values=["segment", "brand", "manufacturer", "state_name", "sub_category", "max_time_month"],
            default_value="segment"
        ),
        SkillParameter(
            name="metric", 
            description="The metrics to aggregate",
            constrained_values=["sales", "volume", "acv", "units", "tdp"],
            is_multi=True,
            default_value=["sales"]
        ),
        SkillParameter(
            name="limit", 
            description="Number of top results to display",
            constrained_values=["5", "10", "15", "20"],
            default_value="10"
        ),
        SkillParameter(
            name="new_metric", 
            description="New metric to add to the chart",
            constrained_values=["sales", "volume", "acv", "units", "tdp"],
            default_value="sales"
        )
    ]
)
def basic_data_bar_chart(skill_input: SkillInput) -> SkillOutput:
    """Creates a bar chart showing top values for any dimension-metric combination"""
    
    load_dotenv()
    
    try:
        # Get parameters
        dimension = skill_input.arguments.dimension
        metrics = skill_input.arguments.metric if isinstance(skill_input.arguments.metric, list) else [skill_input.arguments.metric]
        limit = int(skill_input.arguments.limit)
        
        # Get data
        data = get_chart_data(dimension, metrics, limit)
        
        if data is None or data.empty:
            raise ExitFromSkillException(
                "No data found for the selected dimension and metric combination",
                "No data available for your selection. Please try different parameters."
            )
        
        # Create visualization
        visualization = create_bar_chart(data, dimension, metrics)
        
        # Create export data
        metrics_str = "_".join(metrics)
        export_data = ExportData(
            data=data,
            name=f"{dimension}_by_{metrics_str}"
        )
        
        # Create final prompt
        if len(metrics) == 1:
            metrics_display = format_metric_name(metrics[0]).lower()
        else:
            metrics_display = ", ".join([format_metric_name(m).lower() for m in metrics[:-1]]) + f" and {format_metric_name(metrics[-1]).lower()}"
        
        final_prompt = f"""I've created a bar chart showing the top {limit} {format_dimension_name(dimension).lower()} by {metrics_display}. The chart displays {len(data)} results with clear formatting and tooltips. You can export the underlying data using the "Export Data" option below."""
        
        return SkillOutput(
            visualizations=[visualization],
            export_data=[export_data],
            final_prompt=final_prompt
        )
        
    except ExitFromSkillException:
        raise
    except Exception as e:
        raise ExitFromSkillException(
            f"Error creating bar chart: {str(e)}",
            "Unable to create the bar chart. Please check your parameters and try again."
        )

def get_chart_data(dimension: str, metrics: list, limit: int) -> pd.DataFrame:
    """Retrieves and processes data for the bar chart"""
    
    client = AnswerRocketClient()
    
    # Database context discovery
    is_ar_platform = os.getenv('AR_IS_RUNNING_ON_FLEET')
    try:
        if is_ar_platform:
            skill = client.config.get_copilot_skill()
            if skill is None:
                raise Exception("Failed to retrieve skill context in platform")
                
            dataset = client.data.get_dataset(dataset_id=skill.dataset_id)
            if dataset is None:
                raise Exception("Failed to retrieve dataset metadata from skill context")
                
            database_id = dataset.database.database_id
        else:
            database_id = os.getenv('DATABASE_ID')
            if not database_id:
                raise Exception("DATABASE_ID environment variable not set for local testing")
        
        # Build SQL query with multiple metrics
        metric_selects = [f"SUM({metric}) as total_{metric}" for metric in metrics]
        metric_selects_str = ", ".join(metric_selects)
        
        # Create WHERE conditions to exclude null values for any metric
        where_conditions = [f"{metric} IS NOT NULL" for metric in metrics]
        where_clause = " AND ".join(where_conditions)
        
        # Order by the first metric
        order_metric = metrics[0]
        
        sql_query = f"""
        SELECT 
            {dimension},
            {metric_selects_str}
        FROM w_b6b5_pasta_v8_a65f 
        WHERE {where_clause}
        GROUP BY {dimension}
        ORDER BY total_{order_metric} DESC
        LIMIT {limit}
        """
        
        result = client.data.execute_sql_query(database_id=database_id, sql_query=sql_query)
        if result is None or result.df is None:
            raise Exception("No data returned from SQL query")
        return result.df
        
    except Exception as e:
        raise Exception(f"Database access failed: {str(e)}")

def create_bar_chart(data: pd.DataFrame, dimension: str, metrics: list) -> SkillVisualization:
    """Creates a bar chart visualization using dynamic-layout framework"""
    
    # Prepare data for Highcharts
    categories = data.iloc[:, 0].tolist()  # First column (dimension values)
    
    # Create series data for each metric
    series_data = []
    for i, metric in enumerate(metrics):
        metric_values = data.iloc[:, i + 1].tolist()  # Column i+1 for metric i
        series_data.append({
            "name": format_metric_name(metric),
            "data": metric_values,
            "colorByPoint": len(metrics) == 1  # Only color by point for single metric
        })
    
    # Create title based on metrics
    if len(metrics) == 1:
        title_metrics = format_metric_name(metrics[0])
    else:
        title_metrics = ", ".join([format_metric_name(m) for m in metrics[:-1]]) + f" and {format_metric_name(metrics[-1])}"
    
    # Define the layout structure
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
                }
            },
            {
                "type": "HighchartsChart",
                "name": "SalesChart",
                "parentId": "MainContainer",
                "options": {
                            "chart": {
                                "type": "column",
                                "height": 500
                            },
                            "title": {
                                "text": f"Top {len(data)} {format_dimension_name(dimension)} by {title_metrics}"
                            },
                            "xAxis": {
                                "categories": categories,
                                "title": {
                                    "text": format_dimension_name(dimension)
                                }
                            },
                            "yAxis": {
                                "title": {
                                    "text": title_metrics if len(metrics) == 1 else "Values"
                                },
                                "labels": {
                                    "format": get_axis_format(metrics[0]) if len(metrics) == 1 else "{value:,.0f}"
                                }
                            },
                            "tooltip": {
                                "pointFormat": "<b>{point.y:,.0f}</b><br/>"
                            },
                            "legend": {
                                "enabled": len(metrics) > 1
                            },
                            "plotOptions": {
                                "column": {
                                    "dataLabels": {
                                        "enabled": len(metrics) == 1,
                                        "format": "{point.y:,.0f}"
                                    }
                                }
                            },
                            "series": series_data
                        }
            }
        ]
    }
    
    return SkillVisualization(
        title="Bar Chart",
        layout=json.dumps(layout)
    )

def format_dimension_name(dimension: str) -> str:
    """Formats dimension names for display"""
    name_map = {
        "segment": "Segment",
        "brand": "Brand", 
        "manufacturer": "Manufacturer",
        "state_name": "State",
        "sub_category": "Sub-Category",
        "max_time_month": "Month"
    }
    return name_map.get(dimension, dimension.title())

def format_metric_name(metric: str) -> str:
    """Formats metric names for display"""
    name_map = {
        "sales": "Sales",
        "volume": "Volume",
        "acv": "ACV",
        "units": "Units", 
        "tdp": "TDP"
    }
    return name_map.get(metric, metric.upper())

def get_metric_format(metric: str) -> str:
    """Returns appropriate number format for each metric (for tooltips)"""
    format_map = {
        "sales": "{point.y:$,.0f}",
        "volume": "{point.y:,.0f}",
        "acv": "{point.y:,.1f}",
        "units": "{point.y:,.0f}",
        "tdp": "{point.y:,.1f}"
    }
    return format_map.get(metric, "{point.y:,.0f}")

def get_axis_format(metric: str) -> str:
    """Returns appropriate number format for y-axis labels"""
    format_map = {
        "sales": "${value:,.0f}",
        "volume": "{value:,.0f}",
        "acv": "{value:,.1f}",
        "units": "{value:,.0f}",
        "tdp": "{value:,.1f}"
    }
    return format_map.get(metric, "{value:,.0f}")