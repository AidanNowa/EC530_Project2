from fastapi import FastAPI
from app.routes import dataUpload, training

app = FastAPI()

#include routers from other modules here
app.include_router(dataUpload.router)
app.include_router(training.router)
