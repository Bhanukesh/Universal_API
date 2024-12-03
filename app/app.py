from fastapi import FastAPI
from app.routes.analytics import router as analytics_router
from app.routes.visualize import router as visualize_router

app = FastAPI()

# Include the analytics and visualization routes
app.include_router(analytics_router, prefix="/analytics")
app.include_router(visualize_router, prefix="/visualize")

@app.get("/")
def read_root():
    return {"message": "Welcome to the Universal Analytics API"}
