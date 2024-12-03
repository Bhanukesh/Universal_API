import os
import matplotlib.pyplot as plt
from fastapi import APIRouter, HTTPException
from app.routes.analytics import data_store  # Import the shared data_store

router = APIRouter()

def save_chart(figure, chart_name: str) -> str:
    """Helper function to save chart to a file and return its path."""
    chart_path = os.path.join(os.getcwd(), f"{chart_name}.png")
    figure.savefig(chart_path, format='png')
    plt.close(figure)
    return chart_path

@router.get("/generate-chart")
async def generate_chart(chart_type: str, column: str, filename: str):
    """
    Generates different types of charts for the specified column in the uploaded dataset.

    Args:
        chart_type (str): Type of chart (e.g., 'bar', 'pie', 'line').
        column (str): Column to visualize.
        filename (str): Name of the file in the data_store.

    Returns:
        JSON response with chart details or error message.
    """
    try:
        # Retrieve DataFrame
        df = data_store.get(filename)
        if df is None:
            raise HTTPException(status_code=404, detail=f"File '{filename}' not found in the data store")

        if column not in df.columns:
            raise HTTPException(status_code=400, detail=f"Column '{column}' not found. Available columns: {df.columns.tolist()}")

        # Ensure the column is appropriate for the chart type
        if chart_type == "bar" or chart_type == "pie":
            if not pd.api.types.is_categorical_dtype(df[column]) and not pd.api.types.is_object_dtype(df[column]):
                raise HTTPException(status_code=400, detail=f"Column '{column}' must be categorical for '{chart_type}' chart")

        # Generate Chart
        if chart_type == "bar":
            counts = df[column].value_counts()
            fig = counts.plot(kind='bar', title=f"{chart_type.capitalize()} Chart for {column}", color='skyblue').get_figure()
            chart_path = save_chart(fig, "bar_chart")

        elif chart_type == "pie":
            counts = df[column].value_counts()
            fig, ax = plt.subplots()
            counts.plot(kind='pie', autopct='%1.1f%%', ax=ax, title=f"{chart_type.capitalize()} Chart for {column}")
            chart_path = save_chart(fig, "pie_chart")

        elif chart_type == "line":
            if not pd.api.types.is_numeric_dtype(df[column]):
                raise HTTPException(status_code=400, detail=f"Column '{column}' must be numeric for 'line' chart")
            fig = df[column].plot(kind='line', title=f"{chart_type.capitalize()} Chart for {column}").get_figure()
            chart_path = save_chart(fig, "line_chart")

        else:
            raise HTTPException(status_code=400, detail=f"Unsupported chart type '{chart_type}'. Use 'bar', 'pie', or 'line'")

        return {
            "message": f"{chart_type.capitalize()} chart for column '{column}' generated successfully",
            "chart_path": chart_path
        }
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}
