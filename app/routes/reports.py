'''
1.) Generate Report
    Endpoint: '/reports/{model_id}'
    Method: GET
    Authentication Required: Yes
    Description: Generates a report for a specific model.
    Response: JSON object with report details (ex: performance metrics, usage statistics)
'''

from fastapi import APIRouter, HTTPException, Depends
from typing import Optional
from pydantic import BaseModel
from dependencies import get_current_active_user
from models import User

router = APIRouter(prefix="/reports")

#simulated in-memory storage for reports
reports_db = {}


class ReportDetails(BaseModel):
    model_id: str
    performance_metrics: dict
    usage_statistics: dict

#generate or update a report for a specific model
@router.post("/{model_id}")  #using POST for generation;
async def generate_report(model_id: str, user: User = Depends(get_current_active_user)):
    # TODO: Generate report logic.
    report_data = {
        "performance_metrics": {"accuracy": 0.95, "loss": 0.05},
        "usage_statistics": {"inference_requests": 1000, "average_response_time": "100ms"}
    }
    reports_db[model_id] = report_data  #store or update the report
    return {"message": "Report generated successfully.", "model_id": model_id, "report_details": report_data}

#get report details
@router.get("/{model_id}")
async def get_report(model_id: str, user: User = Depends(get_current_active_user)):
    report = reports_db.get(model_id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return {"model_id": model_id, "report_details": report}

#delete a report
@router.delete("/{model_id}")
async def delete_report(model_id: str, user: User = Depends(get_current_active_user)):
    if model_id not in reports_db:
        raise HTTPException(status_code=404, detail="Report not found to delete")
    del reports_db[model_id]
    return {"message": "Report deleted successfully.", "model_id": model_id}