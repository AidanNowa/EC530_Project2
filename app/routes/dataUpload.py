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

from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from datetime import datetime
from typing import List
from uuid import uuid4
from dependencies import get_current_active_user
from models import User

'''
Creates APIrouter instance which will handle routes related to file uploading
`/upload` will be added before all routes defined in this router, now grouped under a common base path
Tags parameter is used for grouping endpoints in the automatic documentation
'''
router = APIRouter(prefix="/upload", tags=["upload"]) 

#simulated storage for file metadata
file_metadata_db = {}

#simulated function to save files 
async def save_file(file: UploadFile):
    file_id = str(uuid4())
    file_location = f"storage/{file_id}"  #simulate saving to a directory called 'storage'
    with open(file_location, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    return file_id, file.filename
'''
Function takes a list of files as input
Utilizes FasAPIs file upload handling
Returns a JSON object with the filenames of the uploaded files -- placeholder
'''
@router.post("/") # decorator to specify this is a POST endpoint at the path `/upload/`
async def upload_files(files: List[UploadFile] = File(...), user: User = Depends(get_current_active_user)):
    uploaded_files = []
    for file in files:
        file_id, filename = await save_file(file)
        file_metadata_db[file_id] = {"filename": filename, "uploadDate": datetime.now(), "userId": user.username}
        uploaded_files.append({"fileId": file_id, "filename": filename})
    return {"uploadedFiles": uploaded_files}

@router.get("/")
async def list_uploaded_files(user: User = Depends(get_current_active_user)):
    user_files = [metadata for file_id, metadata in file_metadata_db.items() if metadata["userId"] == user.username]
    if not user_files:
        raise HTTPException(status_code=404, detail="No files found for the user")
    return user_files

@router.delete("/{file_id}")
async def delete_file(file_id: str, user: User = Depends(get_current_active_user)):
    if file_id in file_metadata_db:
        if file_metadata_db[file_id]["userId"] != user.username:
            raise HTTPException(status_code=403, detail="Unauthorized to delete this file")
        # TODO: delete the file from the filesystem or cloud storage
        del file_metadata_db[file_id]
        return {"message": "File deleted successfully"}
    else:
        raise HTTPException(status_code=404, detail="File not found")