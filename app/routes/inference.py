'''
1.) Perform Inference
    Endpoint: '/inference/{model_id}'
    Method: POST
    Authentication Required: Yes
    Description: Performs inference on the provided data using the specified model.
    Request Body: Multipart/form-data with the image.
    Response: JSON objec with inference results.
'''

from fastapi import APIRouter, UploadFile, File
from celery_worker import perform_inference_task
import shutil

router = APIRouter(prefix="/inference")

#placeholder for inference logic
@router.post("/{model_id}")
async def perform_inference(model_id: str, file: UploadFile = File(...)):
    #save file to storage system and get a path
    file_location = f"storage/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    #enqueue the celery task
    perform_inference_task.delay(model_id, file_location)
    
    return {"message": "Inference result.", "model_id": model_id}