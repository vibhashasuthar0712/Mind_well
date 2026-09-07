from fastapi import FastAPI

app = FastAPI(title="MindWell API")


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