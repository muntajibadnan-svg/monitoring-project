# 🔍 Production Monitoring Stack

A production-ready monitoring stack built with **Flask**, **Prometheus**, **Grafana**, and **Alertmanager**, fully containerized with Docker Compose.

---

## Architecture

```
┌─────────────┐       ┌──────────────┐       ┌──────────────┐
│  Flask App  │──────▶│  Prometheus  │──────▶│   Grafana    │
│   :5000     │       │    :9090     │       │    :3000     │
│  /metrics   │       │              │       │  Dashboards  │
└─────────────┘       └──────┬───────┘       └──────────────┘
                             │
                      ┌──────▼───────┐       ┌──────────────┐
                      │ Alertmanager │──────▶│ Slack/Email  │
                      │    :9093     │       │ Notifications│
                      └──────────────┘       └──────────────┘

                      ┌──────────────┐
                      │Node Exporter │
                      │    :9100     │
                      └──────────────┘
```

## Features

- ✅ **Structured JSON Logging** — machine-readable logs for aggregation
- ✅ **Prometheus Metrics** — request rate, latency, error rate auto-instrumented
- ✅ **Pre-built Grafana Dashboard** — auto-provisioned, no manual setup
- ✅ **Alerting Rules** — app down, high error rate, high latency, CPU/memory/disk
- ✅ **Health & Readiness Probes** — `/health` and `/ready` endpoints
- ✅ **Multi-stage Docker Build** — minimal image, non-root user
- ✅ **Gunicorn WSGI Server** — production-grade process management
- ✅ **CI/CD Pipeline** — lint, test, build, push, security scan
- ✅ **Resource Limits** — memory and CPU limits on all containers

---

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) (v20.10+)
- [Docker Compose](https://docs.docker.com/compose/install/) (v2.0+)

---

## Quick Start

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd monitoring-project

# 2. Configure environment
cp .env .env.local  # Edit .env with your settings

# 3. Start all services
docker compose up -d

# 4. Verify everything is running
docker compose ps
```

### Access the Services

| Service       | URL                          | Credentials          |
|---------------|------------------------------|----------------------|
| Flask App     | http://localhost:5000        | —                    |
| Prometheus    | http://localhost:9090        | —                    |
| Grafana       | http://localhost:3000        | admin / (see .env)   |
| Alertmanager  | http://localhost:9093        | —                    |
| Node Exporter | http://localhost:9100/metrics| —                    |

---

## Configuration

### Environment Variables (`.env`)

| Variable               | Default      | Description                        |
|------------------------|--------------|------------------------------------|
| `FLASK_ENV`            | `production` | Flask environment                  |
| `FLASK_DEBUG`          | `false`      | Enable debug mode                  |
| `ENABLE_CHAOS`         | `false`      | Enable random crash simulation     |
| `LOG_LEVEL`            | `INFO`       | Logging level (DEBUG/INFO/WARNING) |
| `GUNICORN_WORKERS`     | `4`          | Number of Gunicorn worker processes|
| `GRAFANA_ADMIN_USER`   | `admin`      | Grafana admin username             |
| `GRAFANA_ADMIN_PASSWORD`| `admin`     | Grafana admin password             |

### Alerting Setup

Edit `alertmanager/alertmanager.yml` and replace the placeholder Slack webhook URLs:

```yaml
receivers:
  - name: "default-receiver"
    slack_configs:
      - api_url: "https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK"
```

---

## Project Structure

```
monitoring-project/
├── app.py                     # Flask application
├── gunicorn.conf.py           # Gunicorn production config
├── requirements.txt           # Python dependencies
├── Dockerfile                 # Multi-stage production build
├── docker-compose.yaml        # Full stack orchestration
├── .env                       # Environment variables
├── .dockerignore              # Docker build exclusions
├── prometheus.yml             # Prometheus scrape config
├── alert_rules.yml            # Prometheus alerting rules
├── alertmanager/
│   └── alertmanager.yml       # Alert routing & notifications
├── grafana/
│   ├── dashboards/
│   │   └── app-overview.json  # Pre-built monitoring dashboard
│   └── provisioning/
│       ├── dashboards/
│       │   └── dashboard.yml  # Dashboard provider config
│       └── datasources/
│           └── datasource.yml # Prometheus datasource config
├── tests/
│   └── test_app.py            # Automated test suite
├── .github/
│   └── workflows/
│       └── ci.yml             # CI/CD pipeline
└── README.md
```

---

## Development

### Run Tests Locally

```bash
pip install -r requirements.txt
pytest tests/ -v
```

### Run Linter

```bash
ruff check .
```

### Run App Without Docker (dev mode)

```bash
python app.py
```

---

## Production Deployment Checklist

- [ ] Change `GRAFANA_ADMIN_PASSWORD` in `.env`
- [ ] Configure real Slack/Email webhook in `alertmanager/alertmanager.yml`
- [ ] Set `DOCKER_USERNAME` and `DOCKER_TOKEN` in GitHub Secrets
- [ ] Review resource limits in `docker-compose.yaml` for your server
- [ ] Set up log aggregation (ELK/Loki) for JSON logs
- [ ] Configure TLS/HTTPS (add Nginx reverse proxy if needed)
- [ ] Set up automated backups for Prometheus and Grafana volumes
- [ ] Test alerting end-to-end before going live

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Grafana shows "No data" | Wait 60s for Prometheus to scrape. Check `http://localhost:9090/targets` |
| Flask app won't start | Check logs: `docker compose logs web` |
| Prometheus targets down | Verify service names match in `prometheus.yml` and `docker-compose.yaml` |
| Alertmanager not sending | Check webhook URL. Test with `amtool` CLI |
| High memory usage | Adjust `deploy.resources.limits` in `docker-compose.yaml` |

---

## License

MIT
