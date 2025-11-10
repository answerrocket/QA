import os
import json
import pandas as pd
from dotenv import load_dotenv
from answer_rocket import AnswerRocketClient
from skill_framework import skill, SkillParameter, SkillInput, SkillOutput, SkillVisualization, ExportData, ExitFromSkillException

@skill(
    name="data_table_display",
    description="Displays data in a structured, sortable table format with flexible filtering options",
    parameters=[
        SkillParameter(
            name="dimensions",
            description="The dimensions to include in the table",
            constrained_values=["segment", "brand", "manufacturer", "state_name", "sub_category", "max_time_month"],
            is_multi=True,
            default_value=["segment", "brand"]
        ),
        SkillParameter(
            name="metrics",
            description="The metrics to include in the table",
            constrained_values=["sales", "volume", "acv", "units", "tdp"],
            is_multi=True,
            default_value=["sales", "volume"]
        ),
        SkillParameter(
            name="row_limit",
            description="Maximum number of rows to display",
            constrained_values=["10", "25", "50", "100"],
            default_value="25"
        ),
        SkillParameter(
            name="sort_by",
            description="Column to sort by (defaults to first metric)",
            constrained_values=["sales", "volume", "acv", "units", "tdp"],
            default_value="sales"
        ),
        SkillParameter(
            name="sort_order",
            description="Sort order for the data",
            constrained_values=["desc", "asc"],
            default_value="desc"
        )
    ]
)
def data_table_display(skill_input: SkillInput) -> SkillOutput:
    """Creates a sortable data table with configurable dimensions and metrics"""
    
    load_dotenv()
    
    try:
        # Get parameters
        dimensions = skill_input.arguments.dimensions if isinstance(skill_input.arguments.dimensions, list) else [skill_input.arguments.dimensions]
        metrics = skill_input.arguments.metrics if isinstance(skill_input.arguments.metrics, list) else [skill_input.arguments.metrics]
        row_limit = int(skill_input.arguments.row_limit)
        sort_by = skill_input.arguments.sort_by
        sort_order = skill_input.arguments.sort_order
        
        # Get data
        data = get_table_data(dimensions, metrics, row_limit, sort_by, sort_order)
        
        if data is None or data.empty:
            raise ExitFromSkillException(
                "No data found for the selected dimensions and metrics combination",
                "No data available for your selection. Please try different parameters."
            )
        
        # Create visualization
        visualization = create_data_table(data, dimensions, metrics, sort_by, sort_order)
        
        # Create export data
        dimensions_str = "_".join(dimensions)
        metrics_str = "_".join(metrics)
        export_data = ExportData(
            data=data,
            name=f"data_table_{dimensions_str}_{metrics_str}"
        )
        
        # Create final prompt
        dim_display = format_list_display([format_dimension_name(d) for d in dimensions])
        metric_display = format_list_display([format_metric_name(m) for m in metrics])
        
        final_prompt = f"""I've created a data table showing {dim_display} with {metric_display} data. The table displays {len(data)} rows sorted by {format_metric_name(sort_by)} in {sort_order}ending order. You can sort by any column by clicking the column headers, and export the complete dataset using the "Export Data" option below."""
        
        return SkillOutput(
            visualizations=[visualization],
            export_data=[export_data],
            final_prompt=final_prompt
        )
        
    except ExitFromSkillException:
        raise
    except Exception as e:
        raise ExitFromSkillException(
            f"Error creating data table: {str(e)}",
            "Unable to create the data table. Please check your parameters and try again."
        )

def get_table_data(dimensions: list, metrics: list, row_limit: int, sort_by: str, sort_order: str) -> pd.DataFrame:
    """Retrieves and processes data for the table display"""
    
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
        
        # Map max_time_month to actual column
        dimension_column_map = {
            "max_time_month": "month"
        }
        
        # Build dimension columns
        dimension_columns = []
        for dim in dimensions:
            actual_column = dimension_column_map.get(dim, dim)
            dimension_columns.append(actual_column)
        
        # Build metric aggregations
        metric_selects = [f"SUM({metric}) as total_{metric}" for metric in metrics]
        
        # Create WHERE conditions to exclude null values for any metric
        where_conditions = [f"{metric} IS NOT NULL" for metric in metrics]
        where_clause = " AND ".join(where_conditions)
        
        # Build GROUP BY clause
        group_by_columns = ", ".join(dimension_columns)
        
        # Build ORDER BY clause
        sort_direction = "DESC" if sort_order == "desc" else "ASC"
        
        # Build complete SQL query
        dimension_selects = ", ".join(dimension_columns)
        metric_selects_str = ", ".join(metric_selects)
        
        sql_query = f"""
        SELECT 
            {dimension_selects},
            {metric_selects_str}
        FROM w_b6b5_pasta_v8_a65f 
        WHERE {where_clause}
        GROUP BY {group_by_columns}
        ORDER BY total_{sort_by} {sort_direction}
        LIMIT {row_limit}
        """
        
        result = client.data.execute_sql_query(database_id=database_id, sql_query=sql_query)
        if result is None or result.df is None:
            raise Exception("No data returned from SQL query")
            
        # Rename columns for better display
        df = result.df.copy()
        
        # Rename dimension columns
        for i, dim in enumerate(dimensions):
            actual_column = dimension_column_map.get(dim, dim)
            if actual_column in df.columns:
                df.rename(columns={actual_column: format_dimension_name(dim)}, inplace=True)
        
        # Rename metric columns
        for metric in metrics:
            if f"total_{metric}" in df.columns:
                df.rename(columns={f"total_{metric}": format_metric_name(metric)}, inplace=True)
        
        return df
        
    except Exception as e:
        raise Exception(f"Database access failed: {str(e)}")

def create_data_table(data: pd.DataFrame, dimensions: list, metrics: list, sort_by: str, sort_order: str) -> SkillVisualization:
    """Creates a data table visualization using dynamic-layout framework"""
    
    # Prepare table data
    table_headers = data.columns.tolist()
    table_rows = data.values.tolist()
    
    # Format table data for better display
    formatted_rows = []
    for row in table_rows:
        formatted_row = []
        for i, cell in enumerate(row):
            column_name = table_headers[i]
            # Check if this column represents a metric for formatting
            original_metric = None
            for metric in metrics:
                if format_metric_name(metric) == column_name:
                    original_metric = metric
                    break
            
            if original_metric:
                # Format numeric values based on metric type
                if pd.isna(cell):
                    formatted_row.append("N/A")
                else:
                    formatted_row.append(format_metric_value(cell, original_metric))
            else:
                # Keep dimension values as-is
                formatted_row.append(str(cell) if not pd.isna(cell) else "N/A")
        formatted_rows.append(formatted_row)
    
    # Create table configuration using correct property names
    # Use "columns" and "data" directly on DataTable component
    
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
                "type": "DataTable",
                "name": "DataDisplay",
                "parentId": "MainContainer",
                "columns": table_headers,
                "data": formatted_rows
            }
        ]
    }
    
    return SkillVisualization(
        title="Data Table",
        layout=json.dumps(layout)
    )

def format_list_display(items: list) -> str:
    """Formats a list for display in final prompt"""
    if len(items) == 1:
        return items[0]
    elif len(items) == 2:
        return f"{items[0]} and {items[1]}"
    else:
        return ", ".join(items[:-1]) + f", and {items[-1]}"

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

def format_metric_value(value: float, metric: str) -> str:
    """Formats metric values for table display"""
    if pd.isna(value):
        return "N/A"
    
    format_map = {
        "sales": f"${value:,.0f}",
        "volume": f"{value:,.0f}",
        "acv": f"{value:,.1f}",
        "units": f"{value:,.0f}",
        "tdp": f"{value:,.1f}"
    }
    return format_map.get(metric, f"{value:,.0f}")