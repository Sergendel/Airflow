# Airflow How-To

This document provides quick reference guides for important topics related to Airflow:

1. [Recommended Project Structure for Airflow](#recommended-project-structure-for-airflow)
2. [Purpose of the Compose Folder](#purpose-of-the-compose-folder)
3. [Airflow Batch Jobs vs. Long-Running Services (Port Exposure)](#airflow-batch-jobs-vs-long-running-services-port-exposure)
4. [Running Docker Containers using DockerOperator](#running-docker-containers-using-dockeroperator)
5. [Docker ENTRYPOINT vs. CMD in Airflow](#docker-entrypoint-vs-cmd-in-airflow)

---

## 1. 📁 Recommended Project Structure for Airflow

### **Ideal Structure:**

```
airflow/
├── compose/
│   ├── docker-compose.yaml
│   ├── dags/
│   │   └── my_project/
│   │       ├── my_dag.py
│   │       └── data/
│   │           └── dataset.csv
│   ├── logs/
│   ├── plugins/
│   └── config/
```

### **Best Practices:**

- Keep your **Airflow DAG definitions** in the `dags/` folder.
- Each DAG or pipeline should have its own subfolder for clarity.
- **Do not place entire Python project code directly in the Airflow DAG folder.**

### **Integrating External Python Projects with Airflow:**

- **Dockerize your Python project** and use Airflow's DockerOperator to run it.
- **Package your Python project as a pip-installable package** and install it within Airflow's environment.
- Use Airflow tasks to orchestrate executions or trigger external pipelines rather than embedding large scripts in DAG folders.

This ensures clean separation, maintainability, and scalability of your Airflow-managed workflows.

---

## 2. 📂 Purpose of the Compose Folder

### **Why Use the Compose Folder?**

The `compose/` folder typically contains your Docker Compose files (`docker-compose.yaml`) and related configuration. It's a common and practical way to separate Airflow's Docker deployment from your DAGs, logs, and other resources.

### **Typical Structure:**

```
compose/
├── docker-compose.yaml      # Defines Airflow services
├── dags/                    # Airflow monitors for DAG definitions
├── logs/                    # Airflow logging directory
├── plugins/                 # Airflow plugins (optional)
└── config/                  # Additional configurations (optional)
```

### **Benefits:**

- Clear organization and separation of responsibilities.
- Easy maintenance and scalability.
- Convenient deployment with `docker compose up`.
- Version-control friendly.

---

## 3. 🚩 Airflow Batch Jobs vs. Long-Running Services (Port Exposure)

### **Concept Overview:**

| Type | Lifecycle | Opens Ports? | Suitable for Airflow? |
|------|-----------|--------------|-----------------------|
| Batch Job | Start → Process → End | 🚫 Usually No | ✅ Yes |
| Long-Running Service (API, Webserver) | Start → Run indefinitely | ✅ Usually Yes | 🚫 No |

### **Explanation:**

- **Airflow tasks are batch jobs:**  
  - Clearly defined start and finish.
  - Typically process data files, perform calculations, or trigger pipelines.
  - Usually **do not** open ports or listen for requests.

- **Long-running services:**  
  - Run continuously, exposing ports for communication.
  - Examples: APIs, databases, web servers.
  - **Not suitable** for direct execution in Airflow tasks because Airflow expects tasks to finish.

### **Best Practices:**

- ✅ **Recommended:**  
  - Run batch operations in Airflow tasks without opening ports.

- 🚫 **Not Recommended:**  
  - Running persistent APIs or web servers within Airflow tasks.

- For persistent services:
  - Deploy them externally (Docker Compose, Kubernetes, cloud platforms).
  - Use Airflow tasks to orchestrate interactions with these external services (via APIs, databases, cloud storage, etc.).

---



## 4. 🚀 Running Docker Containers using DockerOperator

### **Overview:**

To effectively run multiple tasks (Extract → Transform → Load) independently using a single Docker image, follow this structure:

### **Step-by-Step Example:**

**Your Python project (`main.py`):**

```python
import sys

def extract():
    print('Extracting data...')

def transform():
    print('Transforming data...')

def load():
    print('Loading data...')

if __name__ == '__main__':
    step = sys.argv[1]

    if step == 'extract':
        extract()
    elif step == 'transform':
        transform()
    elif step == 'load':
        load()
    else:
        raise ValueError('Unknown step.')
```

**Dockerized project (`Dockerfile`):**

```Dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY . .
ENTRYPOINT ["python", "main.py"]
```

**Running Docker containers independently:**

```bash
docker run my_etl_image extract
docker run my_etl_image transform
docker run my_etl_image load
```

### **Airflow DAG definition using separate DockerOperators (Best practice):**

```python
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime

default_docker_config = {
    'image': 'my_etl_image:latest',
    'api_version': 'auto',
    'auto_remove': True,
    'docker_url': 'unix://var/run/docker.sock',
    'network_mode': 'bridge',
}

with DAG(
    'etl_pipeline',
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily',
    catchup=False
) as dag:

    extract_task = DockerOperator(
        task_id='extract',
        command='extract',
        **default_docker_config
    )

    transform_task = DockerOperator(
        task_id='transform',
        command='transform',
        **default_docker_config
    )

    load_task = DockerOperator(
        task_id='load',
        command='load',
        **default_docker_config
    )

    extract_task >> transform_task >> load_task

```

⚠️ **Not Recommended:**
Running all steps as a single task defeats Airflow advantages like individual retries, granular monitoring, and easier debugging.

🚀 **Recommended Approach Summary:**
- Dockerize your project, enabling steps to run independently.
- Define separate Airflow tasks to execute each step separately.

---

# 5. 🐳 Docker ENTRYPOINT vs. CMD in Airflow

### **Key Concepts:**

- **ENTRYPOINT** defines the executable or script Docker runs by default.
- **CMD** provides default arguments to the ENTRYPOINT and can be overridden at runtime.

### **Practical Usage in Airflow:**

- Define ENTRYPOINT clearly in your Dockerfile:

```Dockerfile
ENTRYPOINT ["python", "main.py"]
```

- CMD is optional; Airflow's DockerOperator provides the `command` argument to override CMD:

```python
extract_task = DockerOperator(
    task_id='extract',
    image='my_image:latest',
    command='extract',  # overrides CMD
)
```

- Using Airflow's `command` parameter to pass arguments explicitly to your Docker container is standard practice and recommended.

### **Recommended Approach:**

- Dockerize your project clearly specifying ENTRYPOINT.
- Use Airflow to provide runtime arguments explicitly via the DockerOperator command parameter.
- Avoid embedding complex logic or multiple commands directly within Dockerfiles to maintain clarity and flexibility.

---