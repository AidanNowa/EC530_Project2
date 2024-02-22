from fastapi import FastAPI
from app.routes import dataUpload, training, authenticationAuthorization, dataAnalysis, inference, modelPublishing, reports, testModel

app = FastAPI()

#include routers from other modules here
app.include_router(dataUpload.router)
app.include_router(training.router)
app.include_router(authenticationAuthorization.router)
app.include_router(dataAnalysis.router)
app.include_router(inference.router)
app.include_router(modelPublishing.router)
app.include_router(reports.router)
app.include_router(testModel.router)