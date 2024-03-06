from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime
import uuid

# Load environment variables
load_dotenv()

# MongoDB connection string
MONGODB_URL = "mongodb://localhost:27017"

# Connect to MongoDB
client = MongoClient(MONGODB_URL)

# Select your database
db = client.DIY_ML

# USelect collections
users_collection = db.users
#files_collection = db.files
images_collection = db.images
inferences_collection = db.inferences
models_collection = db.models
reports_collection = db.reports
test_results_collection = db.test_results
training_jobs_collection = db.training_jobs

# make userId, modelId and datasetType fields indexable
users_collection.create_index([("userId", 1)], unique=True)
inferences_collection.create_index([("modelId", 1)], unique=True)
models_collection.create_index([("userId", 1)], unique=True)
images_collection.create_index([("userId", 1), ("datasetType"), 1])

#Insert a new user
def create_user(name, email, hashed_password):
    user_doc = {
        "userId": str(uuid.uuid4()),
        "name": name,
        "email": email,
        "passwordHash": hashed_password,
        "createdAt": datetime.now(),
        "deletedAt": None, #remain as None until deleted
    }
    return users_collection.insert_one(user_doc).inserted_id

#Soft delete a suer by setting the deletedAt field
def soft_delete_user(email):
    return users_collection.update_one(
        {"email": email},
        {"$set": {"deletedAt": datetime.now()}}
    )

#get active users only
def get_active_users():
    return list(users_collection.find({"deletedAt": None}))

# Insert a new file
""" def create_file(user_id, file_name, file_path):
    file_doc = {
        "userId": user_id,
        "fileName": file_name,
        "filePath": file_path,
        "uploadDate": datetime.now(),
    }
    return files_collection.insert_one(file_doc).inserted_id

# Retrieve files for a user
def get_files_by_user(user_id):
    return list(files_collection.find({"userId": user_id})) """




'''
Example of how to add file and view images
# Insert a sample image into the database
image_id = insert_image(
    userId="user123",
    filePath="path/to/image.jpg",
    datasetType="training",
    label="dog",
    polygons=[[10, 10], [100, 10], [100, 100], [10, 100]],
    additionalInfo="Sample image of a dog"
)
print(f"Inserted image ID: {image_id}")

# Retrieve and print all training images for a specific user
training_images = get_images("user123", "training")
for img in training_images:
    print(img)

'''
#insert a new image document
def insert_image(userId, filePath, datasetType, label, polygons, additionalInfo=None):
    image_doc = {
        "userId": userId,
        "createdAt": datetime.now(),
        "filePath": filePath,
        "datasetType": datasetType,
        "metadata": {
            "label": label,
            "polygons": polygons,
            "additionalInfo": additionalInfo
        }
    }
    return images_collection.insert_one(image_doc).inserted_id


# Function to retrieve images by user and dataset type
def get_images(userId, datasetType):
    return list(images_collection.find({"userId": userId, "datasetType": datasetType}))

# Insert a new inference
def create_inference(model_id, input_file_id, result):
    inference_doc = {
        "modelId": model_id,
        "inputFileId": input_file_id,
        "result": result,
        "createdAt": datetime.now(),
    }
    return inferences_collection.insert_one(inference_doc).inserted_id

# Retrieve inferences by model
def get_inferences_by_model(model_id):
    return list(inferences_collection.find({"modelId": model_id}))

# Insert a new model
def create_model(user_id, model_type, database_id, status):
    model_doc = {
        "userId": user_id,
        "modelType": model_type,
        "databaseId": database_id,
        "status": status,
        "createdAt": datetime.now(),
    }
    return models_collection.insert_one(model_doc).inserted_id

# Retrieve models by user
def get_models_by_user(user_id):
    return list(models_collection.find({"userId": user_id}))

# Insert a new report
def create_report(model_id, report_data):
    report_doc = {
        "modelId": model_id,
        "reportData": report_data,
        "createdAt": datetime.now(),
    }
    return reports_collection.insert_one(report_doc).inserted_id

# Retrieve reports by model
def get_reports_by_model(model_id):
    return list(reports_collection.find({"modelId": model_id}))

# Insert new test result
def create_test_result(model_id, accuracy, confusion_matrix):
    test_result_doc = {
        "modelId": model_id,
        "accuracy": accuracy,
        "confusionMatrix": confusion_matrix,
        "createdAt": datetime.now(),
    }
    return test_results_collection.insert_one(test_result_doc).inserted_id

# Retrieve test results by model
def get_test_results_by_model(model_id):
    return list(test_results_collection.find({"modelId": model_id}))

# Insert a new training job
def create_training_job(model_id, parameters, status):
    training_job_doc = {
        "modelId": model_id,
        "parameters": parameters,
        "status": status,
        "startedAt": datetime.now(),
        # Assuming the job starts immediately; adjust as necessary
        "completedAt": None,  # Update this when the job completes
    }
    return training_jobs_collection.insert_one(training_job_doc).inserted_id

# Update a training job's status
def update_training_job_status(job_id, status, completed_at=None):
    update = {"$set": {"status": status}}
    if completed_at:
        update["$set"]["completedAt"] = completed_at
    training_jobs_collection.update_one({"_id": job_id}, update)



