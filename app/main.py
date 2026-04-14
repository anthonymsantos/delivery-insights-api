from fastapi import FastAPI

from .auth_routes import router as auth_router
from .db import engine
from .orm_models import Base
from .routes import router as deliveries_router

app = FastAPI(title="Delivery Insights API", version="0.1.0")

Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(deliveries_router)


@app.get("/")
def root():
    return {"message": "Delivery Insights API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}