'''
1.) Upload Endpoint:
    Endpoint: '/upload'
    Method: POST
    Authentication Required: Yes
    Description: Allows a user to upload image files for a project. Allow multiple files at once?
    Request Body: Multipart/form-data containing the images.
    Response: JSON object with the status of the upload and references to the uploaded images/

2.) List Uploaded Files Endpoint:
    Endpoint: /files
    Method: GET
    Authentication Required: Yes
    Description: Lists all the files uploaded by the user for a project.
    Response: JSON list of files with metadata (e.g., file names, upload dates, sizes).

3.) Delete File Endpoint:
    Endpoint: /files/{file_id}
    Method: DELETE
    Authentication Required: Yes
    Description: Deletes a specified file from the project's dataset.
    Response: JSON object with the status of the deletion.
'''

from fastapi import APIRouter, File, UploadFile, HTTPException
from typing import List

'''
Creates APIrouter instance which will handle routes related to file uploading
`/upload` will be added before all routes defined in this router, now grouped under a common base path
Tags parameter is used for grouping endpoints in the automatic documentation
'''
router = APIRouter(prefix="/upload", tags=["upload"]) 

'''
Function takes a list of files as input
Utilizes FasAPIs file upload handling
Returns a JSON object with the filenames of the uploaded files -- placeholder
'''
@router.post("/") # decorator to specify this is a POST endpointat the parth `/upload/`
async def uploads_files(files: List[UploadFile] = File(...)):
    #TODO: file upload logic
    return {"filenames": [file.filename for file in files]}
