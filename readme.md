# FastAPI CRUD Application

This FastAPI application implements CRUD operations for two entities: **Items** and **User Clock-In Records**. The application utilizes MongoDB for data storage and supports various filtering and aggregation functionalities.

## Table of Contents

- [Prerequisites](#rerequisites)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
- [API Endpoints](#api-endpoints)
- [Test Cases](#test-cases)
- [Authentication](#authentication)

## Prerequisites

- **Python 3.9.13**: Ensure you have Python 3.9.13 installed. You can download it from the [official Python website](https://www.python.org/downloads/release/python-3913/).
- **Docker**(Optional): For running the app as a Dockerized service, install Docker from [here](https://www.docker.com/get-started).

## Features

- Create, Read, Update, and Delete (CRUD) operations for Items and User Clock-In Records.
- Filtering options for retrieving records based on various criteria.
- Aggregation to count items grouped by email.
- Automatic timestamps for record creation.

## Technologies Used

- Python
- FastAPI
- MongoDB
- Pydantic
- uvicorn (ASGI server)

## Setup Instructions

1. **Clone the Repository**

   ```bash
   gh repo clone premkumar1601/TrackIT
   ```
2. **Run the server**

   ```bash
   cd TrackIT
   pip install -r requirements.txt
   uvicorn app.main:app --reload --host 0.0.0.0 --port 80
   ```

   Note: Replace app.env in the project folder with proper env file
3. **Run as Docerised Service**

   ```bash
   docker build -t trackit .
   docker run -d --name trackit -p 80:80  --env-file app.env trackit
   docker logs -f trackit
   ```

## API Endpoints

Please refer to the Swagger UI at `/docs` after starting the application to explore the available endpoints and their functionalities.

## Test Cases

```python
   pytest tests/
```

   This will discover and run all the test cases defined in the tests folder.
   Note: There are 6 test cases written for the Items routes and 6 for the Clock-In routes.

## Authentication

The APIs are authenticated using an API key included in the request headers. This key will be validated against the `API_KEY` provided in the environment file (`app.env`). Ensure that the API key in your environment file matches the expected key for successful authentication.
