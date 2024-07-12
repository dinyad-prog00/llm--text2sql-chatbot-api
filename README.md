# CIAM Data Text2SQL Project

## Overview

Text2SQL is an advanced project designed to convert natural language queries into SQL queries. This application leverages large language models (LLMs) to interpret user queries and interact with a database to fetch and return the desired data. The project is built using FastAPI, providing a robust and scalable server to handle the processing of queries.

## Getting Started

### Option 1: Using LLM API from Google or OpenAI
#### Prerequisites
- Python 3.7+

#### Installation
1. **Clone the repository**:
    ```sh
    git clone git@github.com:adeo/ciam-data--text2sql-api.git
    ```

2. **Create and activate a virtual environment**:
    ```sh
    python -m venv text2sql_venv
    source text2sql_venv/bin/activate   # On Windows, use `text2sql_venv\Scripts\activate`
    ```

3. **Install the dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:

    Create a `.env` file in the root directory and add the following:
    - MODEL_TYPE, type can be `google` or `openai`
    - GOOGLE_API_KEY if using Google ([Get my GOOGLE_API_KEY](https://aistudio.google.com/app/apikey), use your perso gmail)
    - OPENAI_API_KEY if using OpenAI ([Get my OPENAI_API_KEY](https://platform.openai.com/api-keys))
   
5. **Place your Google Cloud Service Account Key (Only if using BigQuery)**:

    Copy from Vault secrets as JSON: `cdp-ciam-admin-console/hmbu/dev/ciam-gcs-dsip.data-read`.
    
    Paste in JSON file and place it in the root directory as `.keys/ciam-gcs-dsip.data-read.json`.

6. **Running the Server**:

    Start the FastAPI server using FastAPI CLI (or [Uvicorn](https://fastapi.tiangolo.com/deployment/server-workers/)):
    ```bash 
    ./text2sql_venv/bin/fastapi dev src/server.py
    ```

    The server will be accessible at `http://localhost:8000`.
    The Swagger docs at `http://localhost:8000/docs`


### Option 2: Running Open Source Model on Conda Env
#### Prerequisites
- Python 3.7+
- [Conda CLI](https://conda.io/projects/conda/en/latest/user-guide/getting-started.html)
- [HuggingFace Account](https://huggingface.co/join)
- Sufficient RAM or GPU memory depending on the size of the model

#### Installation 

1. **Clone the repository**:
    ```sh
    git clone git@github.com:adeo/ciam-data--text2sql-api.git
    ```

2. **Create and activate a Conda environment**:
    [Tensorflow](https://docs.anaconda.com/working-with-conda/applications/tensorflow/)

    ```sh
    conda create -n text2sql_venv tensorflow
    conda activate text2sql_venv
    ```
    Or 

    ```sh
    conda create -n text2sql_venv tensorflow-gpu
    conda activate text2sql_venv
    ```

3. **Install the dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:

    Create a `.env` file in the root directory and add the following:
    - MODEL_TYPE, type can be `pipable` or `chatdb`
    - HF_TOKEN, User Access Token to authenticate to the HuggingFace Hub to pull open source model ([Get my HF_TOKEN](https://huggingface.co/settings/tokens))
    

5. **Place your Google Cloud Service Account Key (Only if using BigQuery)**:

    Copy from Vault secrets as JSON: `cdp-ciam-admin-console/hmbu/dev/ciam-gcs-dsip.data-read`.

    Paste in JSON file and place it in the root directory as `.keys/ciam-gcs-dsip.data-read.json`.

6. **Running the Server**:

    Start the FastAPI server using FastAPI CLI (or [Uvicorn](https://fastapi.tiangolo.com/deployment/server-workers/)):
    ```bash 
    ./text2sql_venv/bin/fastapi dev src/server.py
    ```

    The server will be accessible at `http://localhost:8000`.
    The Swagger docs at `http://localhost:8000/docs`
