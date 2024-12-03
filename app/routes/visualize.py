import os
import matplotlib.pyplot as plt
from fastapi import APIRouter
from app.routes.analytics import data_store  # Import the shared data_store

router = APIRouter()

@router.get("/bar-chart")
async def bar_chart(column: str, filename: str):
    try:
        # Retrieve DataFrame from data_store
        df = data_store.get(filename)
        if df is None:
            return {"error": f"File '{filename}' not found in the data store"}

        if column not in df.columns:
            return {"error": f"Column '{column}' not found. Available columns: {df.columns.tolist()}"}

        # Ensure the column is categorical
        if df[column].dtype not in ['object', 'category']:
            return {"error": f"Column '{column}' must be categorical for generating a bar chart"}

        # Generate bar chart
        counts = df[column].value_counts()
        chart_path = os.path.join(os.getcwd(), "bar_chart.png")  # Save chart in current working directory
        counts.plot(kind='bar', title=f"Distribution of {column}")
        plt.xlabel(column)
        plt.ylabel("Count")
        plt.tight_layout()  # Adjust layout for better appearance
        plt.savefig(chart_path)
        plt.close()

        # Return success message and the path of the saved chart
        return {
            "message": f"Bar chart for column '{column}' generated successfully",
            "chart_path": chart_path
        }
    except KeyError as e:
        return {"error": f"KeyError: {e}. Check the column or filename parameters"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}
