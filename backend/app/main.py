from fastapi import FastAPI
from app.routes.health import router as health_router
from app.routes.upload import router as upload_router
from app.routes.search import router as search_router
from app.routes.coach import router as coach_router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="AI Study Companion API")

app.include_router(health_router)
app.include_router(upload_router)
app.include_router(search_router)
app.include_router(coach_router)

@app.get("/")
def root():
    return {"message": "Backend is running"}
