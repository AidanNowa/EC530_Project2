from fastapi import FastAPI
import db
from app.routes import dataUpload, training, authenticationAuthorization, dataAnalysis, inference, modelPublishing, reports, testModel

app = FastAPI()

@app.lifespan("startup")
async def startup_event():
    db.init_db()  # Initialize the database connection

@app.lifespan("shutdown")
async def shutdown_event():
    db.close_db_client()  # Close the database connection

#include routers from other modules here
app.include_router(dataUpload.router)
app.include_router(training.router)
app.include_router(authenticationAuthorization.router)
app.include_router(dataAnalysis.router)
app.include_router(inference.router)
app.include_router(modelPublishing.router)
app.include_router(reports.router)
app.include_router(testModel.router)

