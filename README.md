# Airflow Projects Repository

Welcome to the Airflow Projects repository, a structured collection of resources, configurations, and helpful notes tailored for managing workflows using Apache Airflow.

---

## 📂 Repository Structure

- **`.idea/`**  
  Configuration files for PyCharm IDE.

- **`MLops notes/`**  
  Documentation and notes related to Machine Learning Operations (MLOps).

- **`compose/`**  
  Contains Docker Compose files and configuration for Airflow setup.

- **`dags/`**  
  Includes several examples and exercises running Airflow DAGs. For example, Exercise 1 is a simple Airflow project where all Python resources are contained within the same DAG/exercise folder, and no Docker was used to run it.

- **`Airflow_cheatcheet.md`**  
  Quick-reference commands, tips, and tricks for working efficiently with Airflow.

---

## 🚀 Getting Started

Follow these steps to quickly set up your Airflow environment:

### Step 1: Navigate to the Docker Compose Directory

```bash
cd compose
```

### Step 2: Launch Airflow Services

Start Airflow webserver, scheduler, and database services using Docker Compose:

```bash
docker-compose up -d
```

### Step 3: Access Airflow Webserver

Open your browser and visit:

```
http://localhost:8080
```

---

## 📚 MLOps Notes

The `MLops notes/` directory contains valuable insights on integrating machine learning pipelines and best practices for using Airflow within your ML workflows. Explore these notes to enhance your understanding of advanced Airflow usage.

---

## 📖 Airflow Cheat Sheet

The `Airflow_cheatcheet.md` provides a quick and handy reference to essential Airflow commands and concepts, helping you streamline workflow development and management.

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. **Fork this repository.**
2. **Create your feature branch** (`git checkout -b feature/my-new-feature`).
3. **Commit your changes** (`git commit -am 'Add new feature'`).
4. **Push to your branch** (`git push origin feature/my-new-feature`).
5. **Open a pull request** explaining your contribution.

---

## 📄 License

This repository is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

For further details about Apache Airflow, visit the [official Airflow GitHub repository](https://github.com/apache/airflow) or the [official Airflow documentation](https://airflow.apache.org/).
