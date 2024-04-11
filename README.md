# EC530_Project2 -- DIY ML

# About

This project aims to explore the development of APIs through the implementation of a "do it yourself" machine learning framework.

Users will be able to upload their own image collections, select a model, and train the model to do image recognition all through the API.

Once their model is trained, users will be able to carry out inferences with uploaded images and obtain reports on their models' accuracy as well as other statistics. 

# Modules

For the following modules, a CRUD model was followed where relevant, meaning that functions to create, read, update, and delete were implemented in modules where their functionality would be necessary.
Current implementations for each function are placeholders as this project focused on API design rather than the functionality of the project. However, error checking and returning error codes has been implemented.

## authenticationAuthroization.py

Handles user authentication and authorization processes, including user registration, login, and token refresh operations. It provides secure access control to the API, ensuring that only registered and authenticated users can perform certain actions.

## dataAnalysis.py

Provides functionality to perform data analysis on user-uploaded datasets. It includes an endpoint to return statistical analysis results, such as image size distribution, helping users understand their data better.

## dataUpload.py

Manages the upload of image files for a project. This module allows users to upload multiple images at once and store them for further processing, like training and inference. It supports operations to list and delete uploaded files, offering full CRUD functionality for file management.

## inference.py

Facilitates the inference process using specified models. Users can submit image files for which the model will perform inference and return predictions. This module integrates with Celery to queue inference tasks, ensuring efficient and scalable processing.

## modelPublishing.py

Enables users to publish their trained models, making them available for inference. It provides endpoints for publishing a model, listing published models, and unpublishing models if needed. This module helps in managing the lifecycle of machine learning models within the application.

## reports.py

Generates and manages reports for specific models. Reports include performance metrics, usage statistics, and other relevant information that provides insights into the model's effectiveness and application usage patterns.

## testModel.py

Supports testing of machine learning models with provided datasets to evaluate their performance. This module offers endpoints to initiate model testing, retrieve test results, including metrics like accuracy and confusion matrix, and supports aborting ongoing tests.

## training.py

Handles the initiation and management of model training jobs. Users can start training with selected models and parameters, check the status of training jobs, and abort them if necessary. This module leverages Celery for queueing and managing long-running training tasks

## main.py

Serves as the entry point for the FastAPI application, integrating all the other modules and setting up the application's routers, middleware, event handlers, and more. It orchestrates the application's components and configurations, ensuring smooth operation.

# Database -- db.py

The module initializes a MongoClient instance to connect to the MongoDB server using a connection string loaded from environment variables, offering security and configurability. It selects the database and defines variables for accessing specific collections like users, images, inferences, and others, facilitating organized data storage and retrieval. 

## Why MongoDB and not SQL?

Schema Flexibility: MongoDB's schema-less nature offers flexibility, allowing for easy modifications of the data model as the application grows without the need for migrations. This is particularly beneficial in the early stages of development and for applications that deal with diverse datasets or rapidly changing data structures.

Document-Oriented Storage: The document model is a natural fit for the JSON-like data structures commonly used in modern web applications. It simplifies the storage and querying of complex, nested data compared to the relational model, making it more intuitive for the expected dataset we would receive (ex: a set of labeled images for detection).

Scalability: MongoDB is designed for scalability, with features like sharding and replication built-in. It can handle large volumes and high throughput of data, making it well-suited for applications that expect to scale, such as those involving image processing and machine learning tasks.

Performance: For many use cases, especially those involving heavy read operations and complex queries across large datasets, MongoDB can offer performance advantages due to its efficient indexing and the ability to serve queries from memory.

# Queuing With Celery

We integrated Celery into the application. Celery is an asynchronous task queue based on distributed message passing, to efficiently manage long-running operations such as model training and inference tasks. This setup allows for the decoupling of computational tasks from the main application flow, improving responsiveness and scalability.

In the application, Celery is configured with a message broker (Redis) to handle message passing between the main application and worker processes. The celery_worker.py module defines task functions that encapsulate the logic for model training and inference. These tasks are enqueued from the FastAPI routes when users initiate actions like starting a training session or submitting an image for inference.

To initiate a Celery task, the application calls .delay() or .apply_async() methods on the task function, passing any required arguments. This non-blocking call immediately returns control to the application, while the task is executed asynchronously by a Celery worker.
