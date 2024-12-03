import os
import matplotlib.pyplot as plt
from fastapi import APIRouter
from app.routes.analytics import data_store  # Import the shared data_store

router = APIRouter()

@router.get("/bar-chart")
async def bar_chart(column: str, filename: str):
    try:
        # Retrieve DataFrame
        df = data_store.get(filename)
        if df is None:
            return {"error": f"File '{filename}' not found in the data store"}
        
        if column not in df.columns:
            return {"error": f"Column '{column}' not found. Available columns: {df.columns.tolist()}"}

        # Ensure the column is categorical
        if df[column].dtype not in ['object', 'category']:
            return {"error": f"Column '{column}' must be categorical for bar chart"}

        # Generate bar chart
        counts = df[column].value_counts()
        chart_path = "bar_chart.png"
        counts.plot(kind='bar', title=f"Distribution of {column}")
        plt.savefig(chart_path)
        plt.close()

        # Return the path of the saved chart
        return {"message": f"Bar chart for column '{column}' generated successfully", "chart_path": chart_path}
    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)}
