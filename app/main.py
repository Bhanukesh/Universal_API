from fastapi import FastAPI
from app.routes import analytics, visualize

app = FastAPI()

# Include the routers
app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
app.include_router(visualize.router, prefix="/visualize", tags=["Visualization"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Universal Analytics API"}
