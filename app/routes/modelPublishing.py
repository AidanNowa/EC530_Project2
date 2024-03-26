'''
1.) Publish Model
    Endpoint: '/model/publish'
    Method: POST
    Authentication Required: Yes
    Description: Publishes a trained model.
    Request Body: JSON object containing 'model_id' and optional 'description'
    Response: JSON object with publication status and model access endpoint
'''

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from dependencies import get_current_active_user
from models import User

router = APIRouter(prefix="/model")

#simulated in-memory storage for published models
published_models_db = {}

class PublishModelRequest(BaseModel):
    model_id: str
    description: Optional[str] = None

#placeholder for model publishing logic
@router.post("/publish")
async def publish_model(request: PublishModelRequest, user: User = Depends(get_current_active_user)):
    if request.model_id in published_models_db:
        raise HTTPException(status_code=400, detail="Model already published")
    # Simulate adding the model to the published models database
    published_models_db[request.model_id] = {"owner": user.username, "description": request.description}
    return {"message": "Model published successfully.", "model_id": request.model_id}

#endpoint to get published model details
@router.get("/{model_id}")
async def get_published_model(model_id: str, user: User = Depends(get_current_active_user)):
    model = published_models_db.get(model_id)
    if not model or model["owner"] != user.username:
        raise HTTPException(status_code=404, detail="Model not found or access denied")
    return {"model_id": model_id, "description": model["description"]}

#endpoint to unpublish a model
@router.delete("/{model_id}")
async def unpublish_model(model_id: str, user: User = Depends(get_current_active_user)):
    model = published_models_db.get(model_id)
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")
    if model["owner"] != user.username:
        raise HTTPException(status_code=403, detail="Unauthorized to unpublish this model")
    del published_models_db[model_id]
    return {"message": "Model unpublished successfully.", "model_id": model_id}