# Airflow How-To

This document provides quick reference guides for important topics related to Airflow:

- [Recommended Project Structure for Airflow](#recommended-project-structure-for-airflow)
- [Running Docker Containers using DockerOperator](#running-docker-containers-using-dockeroperator)
- [Airflow Batch Jobs vs. Long-Running Services (Port Exposure)](#airflow-batch-jobs-vs-long-running-services-port-exposure)
- [Purpose of the Compose Folder](#purpose-of-the-compose-folder)

---

## 📁 Recommended Project Structure for Airflow

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

## 🚀 Running Docker Containers using DockerOperator

### **Step-by-Step Guide:**

#### **1. Prepare your Docker Image**

Build your Docker image locally:

```bash
docker build -t your_image_name:latest .
```

#### **2. Define DockerOperator in your Airflow DAG**

```python
from airflow import DAG
from airflow.providers.docker.operators.docker import DockerOperator
from datetime import datetime

with DAG(
    'docker_example_dag',
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily',
    catchup=False
) as dag:

    run_container = DockerOperator(
        task_id='run_my_container',
        image='your_image_name:latest',
        command='python script.py',
        api_version='auto',
        auto_remove=True,
        docker_url='unix://var/run/docker.sock',
        network_mode='bridge',
        volumes=['/host/path:/container/path'],  # Docker -v
        environment={'MY_ENV_VAR': 'value'},     # Docker -e
        working_dir='/app'                       # Docker -w
    )
```

### **Mapping Docker CLI to DockerOperator:**

| Docker CLI                      | DockerOperator Parameter          | Example                                      |
|---------------------------------|-----------------------------------|----------------------------------------------|
| `-v /host/path:/cont/path`      | `volumes`                         | `volumes=['/host/path:/cont/path']`          |
| `-e VAR=value`                  | `environment`                     | `environment={'VAR': 'value'}`               |
| `--network=my_network`          | `network_mode`                    | `network_mode='my_network'`                  |
| `-w /app`                       | `working_dir`                     | `working_dir='/app'`                         |

### **Key Points:**

- Ensure the Docker socket (`docker.sock`) is accessible from your Airflow environment.
- DockerOperator parameters (`volumes`, `environment`, `network_mode`, `working_dir`) directly match Docker CLI arguments.

---

## 🚩 Airflow Batch Jobs vs. Long-Running Services (Port Exposure)

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

## 📂 Purpose of the Compose Folder

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

**Now you have these key Airflow topics clearly documented and easily accessible!**
