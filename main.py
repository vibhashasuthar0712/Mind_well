from fastapi import FastAPI
from database import Base, engine

app = FastAPI(title="MindWell API")

# Create database tables
Base.metadata.create_all(bind=engine)


@app.get("/")
def home():
    return {
        "message": "MindWell API is running!"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }