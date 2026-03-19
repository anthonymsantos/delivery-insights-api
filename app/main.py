from fastapi import FastAPI
from .routes import router as deliveries_router
from .orm_models import Base
from .db import engine

app = FastAPI(title="Delivery Insights API", version="0.1.0")
Base.metadata.create_all(bind=engine)

app.include_router(deliveries_router)


@app.get("/")
def root():
    return {"message": "Delivery Insights API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}
