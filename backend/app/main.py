from fastapi import FastAPI
from app.routes.health import router as health_router

app = FastAPI(title="AI Study Companion API")

app.include_router(health_router)

@app.get("/")
def root():
    return {"message": "Backend is running"}
