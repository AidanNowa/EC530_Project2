'''
1.) Perform Inference
    Endpoint: '/inference/{model_id}'
    Method: POST
    Authentication Required: Yes
    Description: Performs inference on the provided data using the specified model.
    Request Body: Multipart/form-data with the image.
    Response: JSON objec with inference results.
'''

from fastapi import APIRouter, UploadFile, File, HTTPException
from celery_worker import perform_inference_task
import shutil
import os

router = APIRouter(prefix="/inference")

def get_inference_result(task_id):
    #simulate fetching the inference result.
    return {"status": "Completed", "result": "Cat"}

#placeholder for inference logic
@router.post("/{model_id}")
async def perform_inference(model_id: str, file: UploadFile = File(...)):
    file_location = f"storage/{file.filename}"
    os.makedirs(os.path.dirname(file_location), exist_ok=True)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Enqueue the Celery task and get task_id
    task = perform_inference_task.delay(model_id, file_location)
    
    return {"message": "Inference task enqueued.", "task_id": task.id, "model_id": model_id}

# New endpoint to fetch the result of an inference task
@router.get("/result/{task_id}")
async def get_inference(task_id: str):
    result = get_inference_result(task_id)
    if not result:
        raise HTTPException(status_code=404, detail="Inference result not found")
    return {"task_id": task_id, "result": result}