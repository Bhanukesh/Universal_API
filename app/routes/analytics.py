from fastapi import APIRouter, File, UploadFile
import pandas as pd

router = APIRouter()

data_store = {}

@router.post("/upload-data")
async def upload_data(file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)
        data_store[file.filename] = df
        return {
            "message": "File uploaded successfully",
            "columns": df.columns.tolist(),
            "data_preview": df.head(5).to_dict()
        }
    except Exception as e:
        return {"error": str(e)}

@router.get("/stats")
async def basic_stats(column: str, filename: str):
    try:
        df = data_store.get(filename)
        if df is None:
            return {"error": "File not found"}
        if column not in df.columns:
            return {"error": f"Column '{column}' not found"}
        stats = {
            "mean": df[column].mean(),
            "median": df[column].median(),
            "std_dev": df[column].std(),
        }
        return {"column": column, "stats": stats}
    except Exception as e:
        return {"error": str(e)}
