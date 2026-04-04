# 🚨 MLH Hackathon – Incident Response & Documentation

This repository contains a simple backend application setup for the **MLH Production Engineering Hackathon** challenge focused on **Incident Response & Documentation**.

## 🛠️ Tech Stack

- Python 3.13
- PostgreSQL 15
- Podman (Container Engine)
- uv (Python package manager)

---

## 📂 Project Structure

```
.
├── README.md
├── app
│   ├── config.py
│   ├── database.py
│   ├── models
│   │   └── product.py
│   └── routes
│       └── products.py
├── products.csv
├── pyproject.toml
├── run.py
├── scripts
│   ├── init_db.py
│   └── load_csv.py
└── uv.lock
```

---

## ⚙️ Prerequisites Setup

### 1. Install `uv` (Python Package Manager)

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Reload shell:

```bash
source ~/.bashrc
```

Verify installation:

```bash
uv --version
```

---

### 2. Install Podman

```bash
sudo apt install podman -y
```

Verify:

```bash
podman --version
```

---

### 3. Pull PostgreSQL Image

```bash
podman pull docker.io/library/postgres:15
```

Verify images:

```bash
podman images
```

---

### 4. Run PostgreSQL Container

```bash
podman run -d \
  --name postgres-hackathon \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=hackathon_db \
  -p 5432:5432 \
  -v postgres_data:/var/lib/postgresql/data \
  docker.io/library/postgres:15
```

Check running container:

```bash
podman ps
```

---

### 5. Verify Database Creation

Enter container:

```bash
podman exec -it postgres-hackathon psql -U postgres
```

List databases:

```sql
\l
```

Ensure `hackathon_db` is present.

---

## 🚀 Project Setup

### 1. Install Dependencies

```bash
uv sync
```

---

### 2. Initialize Database Tables

```bash
uv run python -m scripts.init_db
```

---

### 3. Load CSV Data

```bash
uv run python -m scripts.load_csv
```

---

### 4. Run Application

```bash
uv run run.py
```

---

## 📊 Data Source

- `products.csv` – Contains sample product data loaded into PostgreSQL.

---

## 🔍 Features

- Automated DB setup using scripts
- CSV data ingestion
- Modular code structure (models, routes)
- Containerized PostgreSQL setup

---

## 🧪 Troubleshooting

### PostgreSQL not starting

```bash
podman logs postgres-hackathon
```

### Port already in use

```bash
sudo lsof -i :5432
```

Kill process if needed.

### Reset database

```bash
podman rm -f postgres-hackathon
podman volume rm postgres_data
```

---

## 👨‍💻 Author

**Pratik Bapat**

---

## 📄 License

This project is for educational and hackathon purposes.
