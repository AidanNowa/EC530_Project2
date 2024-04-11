'''
1.) Start Training Endpoint:
    Endpoint: /train
    Method: POST
    Authentication Required: Yes
    Description: Initiates the training process for a user's project with the selected model and parameters.
    Request Body: JSON object containing the model selection, training parameters (epochs, batch size, etc.), and references to the dataset.
    Response: JSON object with the training job's status and a unique training job ID.

2.) Training Status Endpoint:
    Endpoint: /train/status/{job_id}
    Method: GET
    Authentication Required: Yes
    Description: Retrieves the status of a specific training job.
    Response: JSON object with details about the training job's progress: epoch, loss, accuracy, etc.   

3.) Abort Training Endpoint: 
    Endpoint: /train/{job_id}
    Method: DELETE
    Authentication Required: Yes
    Description: Aborts a running training job.
    Response: JSON object with the status of the operation.
'''

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field, validator
from typing import List
from uuid import uuid4
from celery.result import AsyncResult
from celery_worker import celery_app, start_training_task
from dependencies import get_current_active_user
from models import User
import os

ALLOWED_FORMATS = ['.csv', '.json', '.txt'] #TODO: add more

router = APIRouter(prefix="/train", tags=["train"])


'''
Pydantic model for the request body
expects a `model_type` and a `parameter`
ensures incoming requests have the correct structure and type of data
helps with automatic request validation
'''
class TrainRequest(BaseModel):
    model_type: str = Field(..., example='CNN')
    parameters: dict = Field(...)

    #field for dataset reference 
    dataset_references: List[str] = Field(...)

@validator('model_type')
def model_type_must_be_known(cls, value):
    #TODO: update with all known types
    known_types = ["CNN", "RNN", "DNN"]
    if value not in known_types:
        raise ValueError(f"model_type must be one of {known_types}")
    return value

@validator('dataset_references')
def dataset_references_must_be_valid(cls, value):
    if not dataset_exists(value):
        raise ValueError(f"Dataset {value} does not exist.")
    if not is_valid_format(value):
        raise ValueError(f"Dataset {value} is not in a valid format.")
    return value

#check if a dataset file exists at the specified path
def dataset_exists(dataset_reference: str) -> bool:
    base_directory = "/path/to/datasets" #TODO: get actual path not placeholder
    dataset_path = os.path.join(base_directory, os.path.basename(dataset_reference))
    return os.path.isfile(dataset_path)

#check if the dataset's format is valid based on the file extension
def is_valid_format(dataset_refernce: str) -> bool:
    _, file_extension = os.path.splitext(dataset_refernce)
    return file_extension in ALLOWED_FORMATS

'''
Defines a route for starting a training process
Takes a `TrainRequest` object as input, automatically parsed and validated by FastAPI from the JSON body of the request
Currently returns a response that includes a message and the `model_type` from the request. --placeholder
'''
@router.post("/")
async def start_training(request: TrainRequest, user: User = Depends(get_current_active_user)):
    #generate a unique job ID
    job_id = str(uuid4())
    #enqueue the training task with Celery
    task = start_training_task.delay(request.model_type, request.parameters, request.dataset_references, job_id)
    # TODO: store or log the task ID and job ID mapping here
    return {"message": "Training started", "model_type": request.model_type, "job_id": job_id}

#getting the status of a training job
@router.get("/status/{job_id}")
async def get_training_status(job_id: str, user: User = Depends(get_current_active_user)):
    # TODO: retrieve task ID for the job ID from storage
    task_result = AsyncResult(job_id, app=celery_app)
    if not task_result:
        raise HTTPException(status_code=404, detail="Training job not found")
    return {"job_id": job_id, "status": task_result.status, "result": task_result.result}

#aborting a training job
@router.delete("/{job_id}")
async def abort_training(job_id: str, user: User = Depends(get_current_active_user)):
    #retrieve and abort the training task
    task_result = AsyncResult(job_id, app=celery_app)
    if not task_result:
        raise HTTPException(status_code=404, detail="Training job not found")
    if task_result.revoke(terminate=True):
        return {"message": "Training aborted successfully", "job_id": job_id}
    else:
        raise HTTPException(status_code=500, detail="Failed to abort training job")