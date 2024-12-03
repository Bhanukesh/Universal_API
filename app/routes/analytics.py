from fastapi import APIRouter, File, UploadFile
import pandas as pd

router = APIRouter()

# Ensure data_store is properly defined
data_store = {}

@router.post("/upload-data")
async def upload_data(file: UploadFile = File(...)):
    try:
        print(f"Uploading file: {file.filename}")
        # Read CSV file into a DataFrame
        df = pd.read_csv(file.file)
        print(f"Data preview:\n{df.head()}")  # Debug log for preview
        
        # Store the DataFrame in the global data_store with the filename as key
        data_store[file.filename] = df
        print(f"File '{file.filename}' successfully stored in data_store")

        # Return success response with details
        return {
            "message": f"File '{file.filename}' uploaded successfully",
            "columns": df.columns.tolist(),
            "data_preview": df.head(5).to_dict()
        }
    except pd.errors.EmptyDataError:
        print("Uploaded file is empty or invalid")  # Debug for empty file
        return {"error": "Uploaded file is empty or invalid"}
    except Exception as e:
        print(f"Error during file upload: {e}")  # Debug general errors
        return {"error": f"An error occurred: {str(e)}"}
