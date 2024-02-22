'''
1.) Test Model
    Endpoint: '/test/{model_id}'
    Method: POST
    Authentication Required: Yes
    Description: Test a model with a provided dataset
    Request Body: Multipart/form-data with test images.
    Response: JSON object with test results (ex: accuracy, confusion matrix)
'''

from fastapi import APIRouter

router = APIRouter(prefix="/test")

#place holder for model testing logic
@router.post("/{model_id}")
async def test_model(model_id: str):
    return {"message": "Test model results.", "model_id": model_id}
