'''
1.) Dataset Statistics
    Endpoint: '/analysis/dataset-stats'
    Method: GET
    Authentication Required: Yes
    Description: Returns statistics about a user's uploaded dataset.
    Response: JSON object with data statistics (ex: image size distribution)
'''

from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from dependencies import get_current_active_user
from models import User, DatasetInfo

router = APIRouter(prefix="/analysis")

def get_dataset_info_for_user(user_id: str) -> DatasetInfo:
    #placeholder function to simulate fetching dataset info, return an empty list if no datasets found
    return DatasetInfo(images=[])

# Function to calculate dataset statistics
def calculate_dataset_statistics(dataset_info: DatasetInfo) -> dict:
    if not dataset_info.images:
        return {"message": "No images in dataset."}
    #placeholder for actual calculation logic ex: calculating image size distribution
    image_sizes = [image.size for image in dataset_info.images]

    average_size = sum(image_sizes) / len(image_sizes) if image_sizes else 0
    return {
        "total_images": len(image_sizes),
        "average_size": average_size,
        # TODO: more statistics as needed
    }

#endpoint to get dataset statistics for the current user
@router.get("/dataset-stats", dependencies=[Depends(get_current_active_user)])
async def dataset_statistics(user: User = Depends(get_current_active_user)):
    dataset_info = get_dataset_info_for_user(user.user_id)
    if not dataset_info:
        raise HTTPException(status_code=404, detail="Dataset not found")
    stats = calculate_dataset_statistics(dataset_info)
    return stats
