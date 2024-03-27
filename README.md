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

