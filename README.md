# **README for ETL Pipeline**

## **Overview**

This project implements a comprehensive ETL (Extract, Transform, Load) pipeline utilizing Docker containers to streamline the process of data extraction from Google Drive, data transformation and validation, and finally data loading into MongoDB. The pipeline is segmented into three primary services: Bronze, Silver, and Gold, each responsible for distinct stages of the ETL process.

## **Architecture**

- **Bronze Service**: Initiates the ETL pipeline by loading data from a specified Google Drive URL and forwarding it to the Silver service for processing.
- **Silver Service**: Transforms the data received from Bronze, performs checks for the existence of domain tables and reference documents, creates them if absent, and appends the necessary IDs to the schema before passing the data to Gold.
- **Gold Service**: Finalizes the pipeline by inserting the transformed and annotated data into MongoDB.

## **Getting Started**

### **Prerequisites**

- Docker and Docker Compose installed on your machine.
- Access to a MongoDB instance (configured through the provided **`docker-compose.yml`**).

### **Running the ETL Pipeline**

1. **Build and Run with Docker Compose**
    
    From the root directory of the project, run:
    
    ```
    docker-compose up --build
    ```
    
    This command builds and starts the Bronze, Silver, and Gold services, along with a MongoDB container. Services will be accessible on ports **`8081-8083`**, and MongoDB will be available on port **`27017`**.

2. **Database Setup Script in Gold**
    
    Go to the gold directory, and under scripts, run the following
    
    ```
    python setup_db.py
    ```
    
    You can do this from inside the docker container or outside. This script creates the reddit_analytics database and its associated collections. 
    
3. **Kick Off the ETL Process**
    
    Send a POST request to **`http://localhost:8081/process-zst`** to initiate the ETL process. This request requires no body.
    
    ```
    curl -X POST http://localhost:8081/process-zst
    ```
    

### **Development in Isolation**

To develop or test a service in isolation:

1. **Build the Docker Image**
    
    Replace **`<service_name>`** with **`bronze`**, **`silver`**, or **`gold`** as appropriate.
    
    ```
    docker build -t <service_name> ./<service_name>
    ```
    
2. **Run the Docker Container**
    
    This command runs the specified service in isolation, defaulting to port **`8080`**.
    
    ```
    docker run -p 8080:8080 <service_name>
    ```
    

### **Environment Variables**

Each service utilizes specific environment variables for configuration:

- **Bronze**:
    - **`GOOGLE_DRIVE_FILE_ID`**: The file ID of the source data on Google Drive.
    - **`SILVER_URL`**: The URL of the Silver service to forward processed data.
- **Silver**:
    - **`GOLD_URL`**: The URL of the Gold service for final data insertion.
    - **`MONGO_DB`**: MongoDB database name (e.g., **`reddit_analytics`**).
    - **`MONGO_INITDB_ROOT_USERNAME`**: Username for MongoDB authentication.
    - **`MONGO_INITDB_ROOT_PASSWORD`**: Password for MongoDB authentication.
- **Gold**:
    - **`MONGO_URI`**: MongoDB connection URI.
    - **`MONGO_DB`**: MongoDB database name for data insertion.

### **Ports Configuration**

- **`8081`**: Bronze service
- **`8082`**: Silver service
- **`8083`**: Gold service
- **`27017`**: MongoDB

## **Docker Compose Services**

The **`docker-compose.yml`** file includes definitions for all services and the MongoDB container, ensuring straightforward deployment and scalability.

## **Volumes**

Persistent data for MongoDB is managed through a named volume, **`mongodb_data_container`**, to maintain data across container restarts.
