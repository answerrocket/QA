import os
import json
import pandas as pd
from dotenv import load_dotenv
from answer_rocket import AnswerRocketClient
from skill_framework import skill, SkillParameter, SkillInput, SkillOutput, SkillVisualization, ExportData, ExitFromSkillException

@skill(
    name="time_series_line_chart",
    description="Creates a line chart showing trends over time with multiple lines for different dimension values",
    parameters=[
        SkillParameter(
            name="dimension",
            description="The dimension to create separate lines for",
            constrained_values=["segment", "brand", "manufacturer", "state_name", "sub_category"],
            default_value="segment"
        ),
        SkillParameter(
            name="metric",
            description="The metric to display on y-axis",
            constrained_values=["sales", "volume", "acv", "units", "tdp"],
            default_value="sales"
        ),
        SkillParameter(
            name="dimension_limit",
            description="Maximum number of dimension values (lines) to display",
            constrained_values=["3", "5", "7", "10"],
            default_value="5"
        )
    ]
)
def time_series_line_chart(skill_input: SkillInput) -> SkillOutput:
    """Creates a line chart showing metric trends over time for different dimension values"""
    
    load_dotenv()
    
    try:
        # Get parameters
        dimension = skill_input.arguments.dimension
        metric = skill_input.arguments.metric
        dimension_limit = int(skill_input.arguments.dimension_limit)
        time_period = skill_input.arguments.time_period
        
        # Get data
        data = get_time_series_data(dimension, metric, dimension_limit, time_period)
        
        if data is None or data.empty:
            raise ExitFromSkillException(
                "No data found for the selected dimension and metric combination",
                "No time series data available for your selection. Please try different parameters."
            )
        
        # Create visualization
        visualization = create_line_chart(data, dimension, metric, time_period)
        
        # Create export data
        export_data = ExportData(
            data=data,
            name=f"{dimension}_{metric}_time_series"
        )
        
        # Create final prompt
        unique_lines = len(data.columns) - 1  # Subtract 1 for date column
        final_prompt = f"""I've created a line chart showing {format_metric_name(metric).lower()} trends over time for the top {unique_lines} {format_dimension_name(dimension).lower()} values. Each line represents a different {format_dimension_name(dimension).lower()}, making it easy to compare trends and identify patterns over the {time_period}ly time period. You can export the underlying data using the "Export Data" option below."""
        
        return SkillOutput(
            visualizations=[visualization],
            export_data=[export_data],
            final_prompt=final_prompt
        )
        
    except ExitFromSkillException:
        raise
    except Exception as e:
        raise ExitFromSkillException(
            f"Error creating line chart: {str(e)}",
            "Unable to create the line chart. Please check your parameters and try again."
        )

def get_time_series_data(dimension: str, metric: str, dimension_limit: int, time_period: str) -> pd.DataFrame:
    """Retrieves and processes time series data for the line chart"""
    
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
        
        # Map time period to SQL expression
        time_column_map = {
            "month": "month",
            "quarter": "'Q' || EXTRACT('quarter' FROM month) || ' ' || EXTRACT('year' FROM month)",
            "year": "EXTRACT('year' FROM month)::text"
        }
        time_expression = time_column_map.get(time_period, "month")
        time_column_alias = f"time_period"
        
        # First, get top dimension values based on total metric
        top_dimensions_query = f"""
        SELECT 
            {dimension},
            SUM({metric}) as total_{metric}
        FROM w_b6b5_pasta_v8_a65f 
        WHERE {metric} IS NOT NULL 
        GROUP BY {dimension}
        ORDER BY total_{metric} DESC
        LIMIT {dimension_limit}
        """
        
        top_result = client.data.execute_sql_query(database_id=database_id, sql_query=top_dimensions_query)
        if top_result is None or top_result.df is None:
            raise Exception("No data returned from top dimensions query")
            
        top_dimension_values = top_result.df.iloc[:, 0].tolist()
        dimension_placeholders = "', '".join(top_dimension_values)
        
        # Now get time series data for these top dimensions
        time_series_query = f"""
        SELECT 
            {time_expression} as {time_column_alias},
            {dimension},
            SUM({metric}) as {metric}_value
        FROM w_b6b5_pasta_v8_a65f 
        WHERE {metric} IS NOT NULL 
            AND {dimension} IN ('{dimension_placeholders}')
        GROUP BY {time_expression}, {dimension}
        ORDER BY {time_expression}, {metric}_value DESC
        """
        
        result = client.data.execute_sql_query(database_id=database_id, sql_query=time_series_query)
        if result is None or result.df is None:
            raise Exception("No data returned from time series query")
            
        # Pivot the data to have time periods as rows and dimension values as columns
        pivoted_data = result.df.pivot(index=time_column_alias, columns=dimension, values=f'{metric}_value').fillna(0)
        
        # Reset index to make time_period a column
        pivoted_data = pivoted_data.reset_index()
        
        return pivoted_data
        
    except Exception as e:
        raise Exception(f"Database access failed: {str(e)}")

def create_line_chart(data: pd.DataFrame, dimension: str, metric: str, time_period: str) -> SkillVisualization:
    """Creates a line chart visualization using dynamic-layout framework"""
    
    # Prepare data for Highcharts
    time_periods = data.iloc[:, 0].tolist()  # First column (time periods)
    dimension_columns = data.columns[1:]     # All columns except first (dimension values)
    
    # Create series data for each dimension value
    series_data = []
    for dim_value in dimension_columns:
        values = data[dim_value].tolist()
        series_data.append({
            "name": str(dim_value),
            "data": values
        })
    
    # Format metric name for display
    metric_formatted = format_metric_name(metric)
    dimension_formatted = format_dimension_name(dimension)
    time_formatted = time_period.capitalize()
    
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
                "name": "TimeSeriesChart",
                "parentId": "MainContainer",
                "options": {
                    "chart": {
                        "type": "line",
                        "height": 500
                    },
                    "title": {
                        "text": f"{metric_formatted} Trends by {dimension_formatted} Over Time"
                    },
                    "xAxis": {
                        "categories": time_periods,
                        "title": {
                            "text": time_formatted
                        }
                    },
                    "yAxis": {
                        "title": {
                            "text": metric_formatted
                        },
                        "labels": {
                            "format": get_axis_format(metric)
                        }
                    },
                    "tooltip": {
                        "pointFormat": "<span style='color:{series.color}'>{series.name}</span>: <b>{point.y:,.0f}</b><br/>"
                    },
                    "legend": {
                        "enabled": True
                    },
                    "plotOptions": {
                        "line": {
                            "dataLabels": {
                                "enabled": False
                            },
                            "marker": {
                                "enabled": True,
                                "radius": 4
                            }
                        }
                    },
                    "series": series_data
                }
            }
        ]
    }
    
    return SkillVisualization(
        title="Time Series Line Chart",
        layout=json.dumps(layout)
    )

def format_dimension_name(dimension: str) -> str:
    """Formats dimension names for display"""
    name_map = {
        "segment": "Segment",
        "brand": "Brand", 
        "manufacturer": "Manufacturer",
        "state_name": "State",
        "sub_category": "Sub-Category"
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