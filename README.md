# 🚨 MLH Hackathon: Incident Response & Observability

This repository contains a containerized Python backend integrated with a full monitoring stack (**Prometheus, Grafana, Alertmanager**) designed for high-availability and rapid incident response.

## 🏗️ Tech Stack

- **Backend:** Python 3.13 (FastAPI/Flask), PostgreSQL 15
- **Infrastructure:** Podman (Container Engine), `uv` (Package Manager)
- **Observability:** Prometheus (Metrics), Grafana (Dashboards), Alertmanager (Incident Alerting)

---

## 🛠️ Prerequisites & Infrastructure (Ubuntu)

### 1. Tooling Setup

```bash
# Install uv (Python Package Manager)
curl -LsSf https://astral.sh/uv/install.sh | sh && source ~/.bashrc

# Install Podman
sudo apt update && sudo apt install podman -y
```

### 2. Database Setup

```bash
# Run PostgreSQL Container
podman run -d --name postgres-hackathon \
  -e POSTGRES_DB=hackathon_db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  -v postgres_data:/var/lib/postgresql/data \
  docker.io/library/postgres:15-alpine

# Initialize App
uv sync
uv run python -m scripts.init_db
uv run python -m scripts.load_csv
```

---

## 🥉 Tier 1: Bronze (The Watchtower)

**Objective:** Eliminate `print()` statements and expose system health.

- **Structured Logging:** All logs are emitted in **JSON format** for machine readability (located in `app/core/logger.py`).
- **Metrics Engine:** Real-time application telemetry is available at `/metrics`.

**Run the App:**
Create a tmux session and inside it run the app so that we can app runs in background and we can access it any time
```bash
tmux new -s hackathon
uv run run.py
```
See live logs again (Reattach):
```bash
tmux attach -t hackathon
```

- **Verify Logs:** Check terminal output for JSON-formatted structured logs.
- **Verify Metrics:** `curl -s http://localhost:5000/metrics`

---

## 🥈 Tier 2: Silver (The Alarm)

**Objective:** Automate failure detection and notify engineers via Discord.

### 1. Start Alerting Stack

```bash
# Launch Alertmanager
podman run -d --name alertmanager \
  -p 9093:9093 \
  -v $(pwd)/monitoring/alertmanager.yml:/etc/alertmanager/alertmanager.yml \
  docker.io/prom/alertmanager:latest

# Launch Prometheus
podman run -d --name prometheus \
  -p 9090:9090 \
  -v $(pwd)/monitoring/prometheus.yml:/etc/prometheus/prometheus.yml \
  -v $(pwd)/monitoring/alerts.yml:/etc/prometheus/alerts.yml \
  docker.io/prom/prometheus:latest
```

### 2. The Fire Drill

To verify the setup, stop the application or simulate a high error rate. If the service stays down for >5 minutes, a notification will fire via the **Discord Webhook** configured in `monitoring/alertmanager.yml`.

---

## 🥇 Tier 3: Gold (The Command Center)

**Objective:** Full situational awareness through visualization.

### 1. Launch Grafana

```bash
mkdir -p grafana-data
podman run -d \
  --name grafana \
  -p 3000:3000 \
  -v $(pwd)/grafana-data:/var/lib/grafana \
  docker.io/grafana/grafana:latest
```

### 2. Dashboard Configuration

1.  Login to `http://localhost:3000` (Default: admin/admin).
2.  Add **Prometheus** (`http://localhost:9090`) as a Data Source.
3.  Import/Create a dashboard to visualize metruics in Grafana

---

## 📂 Project Structure

```text
.
├── app
│   ├── core           # Logger & Metrics logic
│   ├── models         # DB Schema
│   └── routes         # API Endpoints (/products, /health)
├── monitoring         # Config for Prometheus & Alertmanager
├── scripts            # DB Setup & Data Ingestion
├── run.py             # Entry point
└── products.csv       # Seed data
```

## 🔍 API Endpoints

| Method   | Endpoint         | Description              |
| :------- | :--------------- | :----------------------- |
| **GET**  | `/products`      | List all products        |
| **GET**  | `/products/<id>` | Get product by ID        |
| **POST** | `/products`      | Add new product          |
| **GET**  | `/health`        | Application health check |
| **GET**  | `/metrics`       | Prometheus metrics       |

---

## 👨‍💻 Author

**Pratik Bapat**

---

## 📄 License

This project is for educational and hackathon purposes.
