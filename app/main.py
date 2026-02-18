from fastapi import FastAPI
from .routes import router as deliveries_router

app = FastAPI(title="Delivery Insights API", version="0.1.0")

app.include_router(deliveries_router)


@app.get("/")
def root():
    return {"message": "Delivery Insights API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}
