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

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/train", tags=["train"])

'''
Pydantic model for the request body
expects a `model_type` and a `parameter`
ensures incoming requests have the correct structure and type of data
helps with automatic request validation
'''
class TrainRequest(BaseModel):
    model_type: str
    parameters: dict

'''
Defines a route for starting a training process
Takes a `TrainRequest` object as input, automatically parsed and validated by FastAPI from the JSON body of the request
Currently returns a response that includes a message and the `model_type` from the request. --placeholder
'''
@router.post("/")
async def start_training(request: TrainRequest):
    #TODO: training initiation logic based on the request data
    return {"message": "Training started", "model_type": request.model_type}