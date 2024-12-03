from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import matplotlib.pyplot as plt
import os

router = APIRouter()

@router.get("/bar-chart")
async def bar_chart(column: str, filename: str):
    try:
        df = data_store.get(filename)
        if df is None:
            raise HTTPException(status_code=404, detail="File not found")
        if column not in df.columns:
            raise HTTPException(status_code=400, detail=f"Column '{column}' not found")

        chart_path = f"{filename}_bar_chart.png"
        plt.bar(df[column].value_counts().index, df[column].value_counts().values)
        plt.title(f"Bar Chart of {column}")
        plt.xlabel(column)
        plt.ylabel("Frequency")
        plt.savefig(chart_path)
        plt.close()

        return FileResponse(chart_path, media_type="image/png")
    except Exception as e:
        return {"error": str(e)}
    finally:
        if os.path.exists(chart_path):
            os.remove(chart_path)
