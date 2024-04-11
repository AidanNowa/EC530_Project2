'''
1.) Test Model
    Endpoint: '/test/{model_id}'
    Method: POST
    Authentication Required: Yes
    Description: Test a model with a provided dataset
    Request Body: Multipart/form-data with test images.
    Response: JSON object with test results (ex: accuracy, confusion matrix)
'''

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from typing import List
from dependencies import get_current_active_user
from models import User
import uuid
import os

router = APIRouter(prefix="/test")

def sanitize_filename(filename:str) -> str:
    #remove any path characters from finemaes to avoid directory traversal
    filename = filename.replace("/", "").replace("\\", "")
    return filename

#simulated function for saving uploaded test images and returning their file paths
async def save_test_images(files: List[UploadFile]):
    file_paths = []
    for file in files:
        filename = sanitize_filename(file.filename)
        # Create a unique filename to prevent collisions
        file_id = str(uuid.uuid4())
        file_location = f"storage/test_images/{file_id}-{file.filename}"
        os.makedirs(os.path.dirname(file_location), exist_ok=True)
        with open(file_location, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        file_paths.append(file_location)
    return file_paths

#simulated function to perform the model test, returning a placeholder result
def perform_model_test(model_id: str, file_paths: List[str]):
    # TODO: replace with actual logic to test the model with the provided dataset
    return {
        "accuracy": 0.95, #place hodler values
        "confusion_matrix": [[5, 1], [2, 7]]
    }


#place holder for model testing logic
@router.post("/{model_id}")
async def test_model(model_id: str, files: List[UploadFile] = File(...), user: User = Depends(get_current_active_user)):
    if not files:
        raise HTTPException(status_code=400, detail="No test images provided")
    
    #save uploaded files and get their paths
    file_paths = await save_test_images(files)
    
    #simulate testing the model with saved images
    test_results = perform_model_test(model_id, file_paths)
    
    #cleanup test images after processing if needed
    #for file_path in file_paths:
    #    os.remove(file_path)
    
    return {"message": "Test completed successfully", "model_id": model_id, "test_results": test_results}